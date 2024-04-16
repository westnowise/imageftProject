from django.urls import path
from . import views
from django.urls import path
# from .views import index, capture_image

urlpatterns = [
    path('image/', views.index, name='image'),
    path('capture/', views.capture_image, name='capture_image'),
]