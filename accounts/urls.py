from django.urls import path
from .views import *

app_name = 'accounts' 

urlpatterns = [
    path('', start, name='start'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    # path('', main, name='main'),
]