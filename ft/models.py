from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class FairyTale(models.Model):   
    fairytale_id = models.AutoField(primary_key=True)  
    title = models.CharField(max_length=20, null=True)     
    image = models.BinaryField(null=True, blank=True)     
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True) # user 삭제 시 model 삭제
    date = models.DateField(default=timezone.now)