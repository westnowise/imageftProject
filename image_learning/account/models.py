from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # 여기에 추가 필드를 정의합니다.
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='user_images/', blank=True, null=True)

    # 이 필드가 사용자를 식별하는 데 사용되는 고유한 식별자임을 설정합니다.
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
