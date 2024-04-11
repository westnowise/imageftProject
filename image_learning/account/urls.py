from django.urls import path
from . import views
from django.urls import path
# from .views import index, capture_image

urlpatterns = [
    path('signup/', views.signup, name='signup'),
]