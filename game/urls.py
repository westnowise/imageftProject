# urls.py
from django.urls import path
from . import views
urlpatterns = [
    path('video_stream/', views.video_stream, name='video_stream'),
    path('', views.game, name='game_page'),
    path('check_camera_status/', views.check_camera_status, name='check_camera_status'),  # 카메라 상태 체크 엔드포인트 추가
]