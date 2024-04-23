from django.urls import path
from . import views
from django.urls import path
# from .views import index, capture_image

urlpatterns = [
    path('image/', views.index, name='image'),
    path('capture/', views.capture_image, name='capture_image'),
    path('save/', views.save_image, name='save_image'),
    path('video/', views.index, name='index2'),
    path('userpage/', views.userpage, name='userpage'),
]