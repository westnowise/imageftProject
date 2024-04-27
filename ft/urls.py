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
    path('goods', views.goods, name='goods'),
    path('get-images/', views.get_images, name='get-images'),
    # path('cal_db', views.cal_db, name='cal_db'),
    path('gallery', views.gallery, name='gallery'),
    

    # path('gallery', views.userpage, name='gallery'),
]