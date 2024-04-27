from django.shortcuts import render
from ft.models import FairyTale 
import base64
import cv2
import os
import numpy as np
import moviepy.editor as mp
from django.contrib import messages
import threading
from django.conf import settings

def main(request):
    return render(request, 'main/main.html')

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        # 사용자의 FairyTale 객체 정보를 조회
        user_fairytales = FairyTale.objects.filter(user=request.user)

         # 바이너리 이미지 데이터를 Base64로 인코딩하여 템플릿에 전달
        for fairy_tale in user_fairytales:
            if fairy_tale.image:
                fairy_tale.base64_image = base64.b64encode(fairy_tale.image).decode('utf-8')


        # 템플릿에 전달할 컨텍스트 데이터
        context = {
            'user_fairytales': user_fairytales,
            'next_page': 'main2'
        }

        return render(request, 'main/index.html', context)
    else:
        return render(request, 'main/index.html')

def mosaic_frame(frame, webcam_image_resized, target_color_hsv, tolerance=30):
    # Convert frame to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Calculate lower and upper bounds for the target color
    # lower_bound = np.array([target_color_hsv[0] - tolerance, 50, 50])
    # upper_bound = np.array([target_color_hsv[0] + tolerance, 255, 255])

    lower_bound = np.array([target_color_hsv[0] - tolerance, target_color_hsv[1]- tolerance,target_color_hsv[2]- tolerance])
    upper_bound = np.array([target_color_hsv[0] + tolerance, target_color_hsv[1]+ tolerance,target_color_hsv[2]+ tolerance])


    # Threshold the HSV image to get only the target color
    mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)

    # Find contours of regions with the target color
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Get the center of each region and paste the webcam image at that center
    for contour in contours:
        # Calculate the center of the contour
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            # Get dimensions of the webcam image
            webcam_h, webcam_w = webcam_image_resized.shape[:2]

            # Calculate coordinates to paste the webcam image at the center of the contour
            x1 = max(cX - webcam_w // 2, 0)
            y1 = max(cY - webcam_h // 2, 0)
            x2 = min(cX + webcam_w // 2, frame.shape[1])
            y2 = min(cY + webcam_h // 2, frame.shape[0])

            # Extract the alpha channel from the webcam image
            alpha_channel = webcam_image_resized[:, :, 3] / 255.0

            # Calculate the region of interest on the frame
            roi = frame[y1:y2, x1:x2]

            # Resize the alpha channel to match the ROI size
            resized_alpha_channel = cv2.resize(alpha_channel, (roi.shape[1], roi.shape[0]))

            # Merge the resized alpha channel with the frame ROI
            merged_roi = (roi * (1 - resized_alpha_channel[:, :, np.newaxis]) +
                          webcam_image_resized[:roi.shape[0], :roi.shape[1], :3] * (resized_alpha_channel[:, :, np.newaxis]))

            # Update the frame with the merged ROI
            frame[y1:y2, x1:x2] = merged_roi

    return frame


def main2(request):
    static_dir = settings.STATIC_ROOT or settings.STATICFILES_DIRS[0]
    cap_path = os.path.join(static_dir, 'img/vd2.mp4')
    webimg_path = os.path.join(static_dir, 'img/removed_bg_image.png')
    output_folder = os.path.join(static_dir, 'video')
    os.makedirs(output_folder, exist_ok=True)
    output_video_path = os.path.join(output_folder, 'output.mp4')
    final_output_path = os.path.join(output_folder, 'final_output.mp4')

    try:
        cap = cv2.VideoCapture(cap_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        webcam_image = cv2.imread(webimg_path, cv2.IMREAD_UNCHANGED)
        h, w = webcam_image.shape[:2]
        target_color_bgr = (0, 244, 34)
        target_color_hsv = cv2.cvtColor(np.uint8([[target_color_bgr]]), cv2.COLOR_BGR2HSV)[0][0]
        
        out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (int(cap.get(3)), int(cap.get(4))))

        while(cap.isOpened()):
            ret, frame = cap.read()
            if not ret:
                break

            frame = mosaic_frame(frame, webcam_image, target_color_hsv)  # 이 부분에서 성능 최적화 필요
            out.write(frame)
    finally:
        cap.release()
        out.release()
        cv2.destroyAllWindows()

    # 동영상과 오디오 합성
    video = mp.VideoFileClip(output_video_path)
    audio = mp.AudioFileClip(cap_path)
    final_clip = video.set_audio(audio)
    final_clip.write_videofile(final_output_path)

    messages.success(request, '영상 저장이 완료되었습니다.')
    return render(request, 'main/index2.html', {'video_url': os.path.join('video', 'final_output.mp4')})

def main3(request):
    static_dir = settings.STATIC_ROOT or settings.STATICFILES_DIRS[0]
    cap_path = os.path.join(static_dir, 'img/vd3.mp4')
    webimg_path = os.path.join(static_dir, 'img/removed_bg_image.png')
    output_folder = os.path.join(static_dir, 'video')
    os.makedirs(output_folder, exist_ok=True)
    output_video_path = os.path.join(output_folder, 'output.mp4')
    final_output_path = os.path.join(output_folder, 'final_output.mp4')

    try:
        cap = cv2.VideoCapture(cap_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        webcam_image = cv2.imread(webimg_path, cv2.IMREAD_UNCHANGED)
        h, w = webcam_image.shape[:2]
        target_color_bgr = (0, 244, 34)
        target_color_hsv = cv2.cvtColor(np.uint8([[target_color_bgr]]), cv2.COLOR_BGR2HSV)[0][0]
        
        out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (int(cap.get(3)), int(cap.get(4))))

        while(cap.isOpened()):
            ret, frame = cap.read()
            if not ret:
                break

            frame = mosaic_frame(frame, webcam_image, target_color_hsv)  # 이 부분에서 성능 최적화 필요
            out.write(frame)
    finally:
        cap.release()
        out.release()
        cv2.destroyAllWindows()

    # 동영상과 오디오 합성
    video = mp.VideoFileClip(output_video_path)
    audio = mp.AudioFileClip(cap_path)
    final_clip = video.set_audio(audio)
    final_clip.write_videofile(final_output_path)

    messages.success(request, '영상 저장이 완료되었습니다.')
    return render(request, 'main/index3.html', {'video_url': os.path.join('video', 'final_output.mp4')})

def main4(request):
    static_dir = settings.STATIC_ROOT or settings.STATICFILES_DIRS[0]
    cap_path = os.path.join(static_dir, 'img/vd4.mp4')
    webimg_path = os.path.join(static_dir, 'img/removed_bg_image.png')
    output_folder = os.path.join(static_dir, 'video')
    os.makedirs(output_folder, exist_ok=True)
    output_video_path = os.path.join(output_folder, 'output.mp4')
    final_output_path = os.path.join(output_folder, 'final_output.mp4')

    try:
        cap = cv2.VideoCapture(cap_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        webcam_image = cv2.imread(webimg_path, cv2.IMREAD_UNCHANGED)
        h, w = webcam_image.shape[:2]
        target_color_bgr = (0, 244, 34)
        target_color_hsv = cv2.cvtColor(np.uint8([[target_color_bgr]]), cv2.COLOR_BGR2HSV)[0][0]
        
        out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (int(cap.get(3)), int(cap.get(4))))

        while(cap.isOpened()):
            ret, frame = cap.read()
            if not ret:
                break

            frame = mosaic_frame(frame, webcam_image, target_color_hsv)  # 이 부분에서 성능 최적화 필요
            out.write(frame)
    finally:
        cap.release()
        out.release()
        cv2.destroyAllWindows()

    # 동영상과 오디오 합성
    video = mp.VideoFileClip(output_video_path)
    audio = mp.AudioFileClip(cap_path)
    final_clip = video.set_audio(audio)
    final_clip.write_videofile(final_output_path)

    messages.success(request, '영상 저장이 완료되었습니다.')
    return render(request, 'main/index4.html', {'video_url': os.path.join('video', 'final_output.mp4')})