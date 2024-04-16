from django.shortcuts import render
from ft.models import FairyTale 
import base64
import cv2
import pygame
from pygame.locals import *


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
            'user_fairytales': user_fairytales
        }

        return render(request, 'main/index.html', context)
    else:

        return render(request, 'main/index.html')
    

def video_player(request):

    # Pygame 초기화
    pygame.init()

    # 동영상 표시할 창 크기 (영상의 원본 크기로 설정)
    display_width = 1280  # 예시로 1280x720 크기로 설정
    display_height = 720

    # Pygame 창 생성
    screen = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('Video with Button')

    # 비디오 파일 경로
    video_path = '빵빵이의 태껀도 ~!.mp4'

    # 비디오 파일 열기
    cap = cv2.VideoCapture(video_path)

    # 동영상 재생 플래그
    video_playing = True

    # 버튼 이미지 로드 및 크기 조정
    button_image = pygame.image.load('images/back_button.png')
    button_image = pygame.transform.scale(button_image, (50, 50))  # 이미지 크기 조정
    button_rect = button_image.get_rect(topleft=(10, 10))  # 이미지 위치 설정

    # 팝업 배경 이미지 로드
    popup_bg = pygame.image.load('images/팝업_배경.png')
    popup_bg_rect = popup_bg.get_rect(center=(display_width // 2, display_height // 2))  # 중앙 정렬

    # 팝업 표시 여부
    show_popup = False

    # 팝업 표시 함수
    def display_popup():
        screen.blit(popup_bg, popup_bg_rect)

    # 비디오 재생
    while cap.isOpened():
        ret, frame = cap.read()  # 비디오로부터 프레임 읽기

        if not ret:
            print("Video ended.")
            break

        # 프레임 변환 (OpenCV에서 numpy 배열을 Pygame 이미지로 변환)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = pygame.image.frombuffer(frame.tobytes(), (int(cap.get(3)), int(cap.get(4))), 'RGB')

        # 프레임 표시
        screen.blit(frame, (0, 0))

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == QUIT:
                cap.release()
                pygame.quit()
                quit()
            elif event.type == MOUSEBUTTONDOWN:
                # 마우스 왼쪽 버튼 클릭 시 back_button 이미지를 클릭한 경우
                if button_rect.collidepoint(event.pos):
                    video_playing = not video_playing
                    if not video_playing:
                        show_popup = True  # 일시 정지 상태에서 팝업 표시
                    else:
                        show_popup = False  # 일시 정지 상태 해제 시 팝업 숨기기

        # 동영상 일시 정지 상태인 경우 팝업 표시
        if show_popup:
            display_popup()

        # 동영상 일시 정지/재생
        if not video_playing:
            cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_POS_FRAMES) - 1)  # 현재 프레임 이전 프레임으로 되돌리기

        # 버튼 표시
        screen.blit(button_image, button_rect)

        pygame.display.flip()

        # 원래 동영상 속도로 조절 (대략 30fps)
        pygame.time.delay(int(1000 / 30))

    # 비디오 재생이 끝나면 비디오 캡처 객체 해제

    cap.release()

    # Pygame 종료
    pygame.quit()

    return render(request, 'main/index.html')