from django.shortcuts import render

# Create your views here.
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import time
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def index(request):
    static_dir = settings.STATIC_ROOT or settings.STATICFILES_DIRS[0]  # 예제로 첫 번째 STATICFILES_DIRS 사용
    hat_path = os.path.join(static_dir, 'img/game/red_hood(2).png')
    basket_path = os.path.join(static_dir, 'img/game/target.png')
    success_path = os.path.join(static_dir, 'img/game/success.png')
    fail_path = os.path.join(static_dir, 'img/game/fail.png')
    money_path = os.path.join(static_dir, 'img/game/money')

    # 로깅으로 경로 확인
    logger.debug(f"Attempting to load hat image from: {hat_path}")
    logger.debug(f"Attempting to load basket image from: {basket_path}")
    logger.debug(f"Attempting to load success image from: {success_path}")
    logger.debug(f"Attempting to load fail image from: {fail_path}")
    logger.debug(f"Loading money images from: {money_path}")

    # 이미지 로드 및 알파 채널 추가 함수
    def add_alpha_channel(img):
        if img is None:
            logger.error("Failed to load image.")
            raise ValueError("Failed to load image, received None.")
        if img.shape[2] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
        return img

    try:
        hat = cv2.imread(hat_path, cv2.IMREAD_UNCHANGED)
        basket = cv2.imread(basket_path, cv2.IMREAD_UNCHANGED)
        success_img = add_alpha_channel(cv2.imread(success_path, cv2.IMREAD_UNCHANGED))
        fail_img = add_alpha_channel(cv2.imread(fail_path, cv2.IMREAD_UNCHANGED))
    except Exception as e:
        logger.error(f"Error loading images: {str(e)}")
        return render(request, 'error.html', {'error_message': str(e)})

    # 웹캠 설정
    cap = cv2.VideoCapture(0)
    frame_width, frame_height = 1280, 720
    cap.set(3, frame_width)
    cap.set(4, frame_height)
    detector = HandDetector(detectionCon=0.8)

    # 한글 텍스트 그리기 함수
    def draw_korean_text(img, text, font_size, font_color, x_start, y_start):
        img_pil = Image.fromarray(img)
        draw = ImageDraw.Draw(img_pil)
        font_path= os.path.join(static_dir, 'img/game/ttf/KCC-Chassam.ttf')
        font = ImageFont.truetype(font_path, size=font_size)
        draw.text((x_start, y_start), text, fill=font_color, font=font)
        return np.array(img_pil)

    # 모자 위치 고정 함수
    def put_fixed_hat(img, hat, frame_width, frame_height):
        x_start, x_end = int(frame_width / 4), int(frame_width * 3 / 4)
        y_start, y_end = 0, frame_height
        hat_resized = cv2.resize(hat, (x_end - x_start, y_end - y_start))
        hat_alpha = hat_resized[:, :, 3] / 255.0
        hat_part_resized = hat_resized[:, :, :3]
        img_part = img[y_start:y_end, x_start:x_end]
        img_part_masked = img_part * (1.0 - hat_alpha)[:, :, np.newaxis]
        blended_hat = hat_part_resized * hat_alpha[:, :, np.newaxis]
        img[y_start:y_end, x_start:x_end] = (img_part_masked + blended_hat).astype(np.uint8)
        return img

    # 이미지 드래그 가능 클래스
    class DragImg():
        def __init__(self, path, posOrigin, imgType):
            self.posOrigin = posOrigin
            self.imgType = imgType
            self.path = path
            self.isSelected = False
            self.img = cv2.imread(self.path, cv2.IMREAD_UNCHANGED if imgType == 'png' else cv2.IMREAD_COLOR)
            self.size = self.img.shape[:2]
            self.img = cv2.resize(self.img, (150, 150))
            self.adjustPosition()

        def adjustPosition(self):
            edge_margin = 50
            if self.posOrigin[0] < edge_margin:
                self.posOrigin[0] = edge_margin
            elif self.posOrigin[0] + self.size[1] > frame_width - edge_margin:
                self.posOrigin[0] = frame_width - self.size[1] - edge_margin
            if self.posOrigin[1] < edge_margin:
                self.posOrigin[1] = edge_margin
            elif self.posOrigin[1] + self.size[0] > frame_height - edge_margin:
                self.posOrigin[1] = frame_height - self.size[0] - edge_margin

        def update(self, cursor, isSelected=False):
            if isSelected:
                self.posOrigin = cursor[0] - self.size[1] // 2, cursor[1] - self.size[0] // 2

    # 이미지 목록 로드
    # path = "../static/img/game/money"

    myList = os.listdir(money_path)
    listImg = [DragImg(f'{money_path}/{pathImg}', [50 + i * 300, 50], 'png' if 'png' in pathImg else 'jpg') for i, pathImg in enumerate(myList)]

    selectedImg = None

    # 목표 이미지 설정 및 크기 조절
    target_path = os.path.join(static_dir, 'img/game/target.png')
    target_img = cv2.imread(target_path, cv2.IMREAD_UNCHANGED)
    x_start, x_end = int(frame_width/4), int(frame_width*3/4)
    y_start, y_end = int(frame_height*4/5), frame_height
    target_img = cv2.resize(target_img, (x_end - x_start, y_end - y_start), interpolation=cv2.INTER_AREA)
    target_pos = (frame_width // 2 - target_img.shape[1] // 2, frame_height - target_img.shape[0])
    target_size = target_img.shape[:2]

    # 결과 표시 및 리셋 관리
    show_result = False
    start_reset_time = None
    result_image = None

    while True:
        success, img = cap.read()
        if not success:
            break

        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img, flipType=False)
        img = draw_korean_text(img, "바구니에 필요한 만큼의 돈을 담아주세요!", 50, (0, 0, 0), int(frame_width/5), 20)
        img = put_fixed_hat(img, hat, frame_width, frame_height)

        # 목표 이미지 화면 표시
        overlay = img[target_pos[1]:target_pos[1] + target_size[0], target_pos[0]:target_pos[0] + target_size[1]]
        mask = target_img[:, :, 3]
        mask = cv2.resize(mask, (overlay.shape[1], overlay.shape[0]), interpolation=cv2.INTER_AREA)
        mask = cv2.normalize(mask, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        mask_inv = cv2.bitwise_not(mask)
        background = cv2.bitwise_and(overlay, overlay, mask=mask_inv)
        foreground = cv2.bitwise_and(target_img[:, :, :3], target_img[:, :, :3], mask=mask)
        combined = cv2.add(background, foreground)
        img[target_pos[1]:target_pos[1] + target_size[0], target_pos[0]:target_pos[0] + target_size[1]] = combined

        # 손 인식 및 드래그 로직
        if hands:
            lmList = hands[0]['lmList']
            length, info, img = detector.findDistance(lmList[8][:2], lmList[12][:2], img)
            cursor = lmList[8][:2]
            fingerDistance = detector.findDistance(lmList[8][:2], lmList[5][:2])[0]

            if length < 80 and fingerDistance > 80:
                if selectedImg is None:
                    for imgObject in listImg:
                        ox, oy = imgObject.posOrigin
                        w, h = imgObject.size
                        if ox < cursor[0] < ox + w and oy < cursor[1] < oy + h:
                            imgObject.isSelected = True
                            selectedImg = imgObject
                            break
                else:
                    selectedImg.update(cursor, True)
                    if (target_pos[0] < cursor[0] < target_pos[0] + target_size[1] and
                        target_pos[1] < cursor[1] < target_pos[1] + target_size[0]):
                        if selectedImg.path.endswith("money1.png"):
                            result_image = success_img
                        else:
                            result_image = fail_img
                        show_result = True
                        start_reset_time = time.time()
                    selectedImg.isSelected = False
                    selectedImg = None
            else:
                if selectedImg is not None:
                    selectedImg.isSelected = False
                    selectedImg = None

        # 결과 이미지 표시
        if show_result:
            img = cvzone.overlayPNG(img, result_image, [frame_width // 2 - result_image.shape[1] // 2, frame_height // 2 - result_image.shape[0] // 2])
            if result_image is fail_img and time.time() - start_reset_time > 2:
                # 리스트 및 선택된 이미지 초기화
                listImg = [DragImg(f'{money_path}/{pathImg}', [50 + i * 300, 50], 'png' if 'png' in pathImg else 'jpg') for i, pathImg in enumerate(myList)]
                selectedImg = None
                show_result = False
                start_reset_time = None
                result_image = None
        
        if show_result:
            img = cvzone.overlayPNG(img, result_image, [frame_width // 2 - result_image.shape[1] // 2, frame_height // 2 - result_image.shape[0] // 2])
            if result_image is success_img and time.time() - start_reset_time > 3:
                break  # 성공 이미지 표시 후 3초 후 종료

        for imgObject in listImg:
            img = cvzone.overlayPNG(img, imgObject.img, [imgObject.posOrigin[0], imgObject.posOrigin[1]])

        # for imgObject in listImg:
        #     h, w = imgObject.size
        #     ox, oy = imgObject.posOrigin
        #     if imgObject.imgType == "png":
        #         img = cvzone.overlayPNG(img, imgObject.img, [ox, oy])
        #     else:
        #         img[oy:oy + h, ox:ox + w] = imgObject.img

        cv2.imshow("Interactive Display", img)
        key = cv2.waitKey(1)
        if key == ord("q") or key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    return render(request, 'main/index.html', {
        'listImg': listImg,
        'target_pos': target_pos,
        'target_size': target_size,
    })