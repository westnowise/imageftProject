from django.urls import path
from . import views


urlpatterns = [
    path('start', views.main, name='main'),
    path('main', views.index, name='index'),
    path('main2', views.main2, name='main2'),
    path('main3', views.main3, name='main3'),
    path('main4', views.main4, name='main4'),
]