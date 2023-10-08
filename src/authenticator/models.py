from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone
from authenticator.manager import UserManager
import uuid

# Create your models here.

def profilePicPath(obj, filename:str):
    ext = filename.split('.')[-1]
    uid = uuid.uuid4()
    return \
        f'uploads/{obj.username}/profile_pictures/profile_picture_{uid}.{ext}'

# class UserExtend(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     phone_number = models.CharField(max_length=12, unique=True)
#     birthdate = models.DateField()

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=12, unique=True)
    dob = models.DateField(null=True, blank=True)
    about = models.CharField(max_length=140, null=True, blank=True)
    profile_pic = models.ImageField(upload_to=profilePicPath, null=True, blank=True)
    REQUIRED_FIELDS = []

    objects = UserManager()

    # class Meta:
    #     # db_table = 'auth_user'
    #     app_label = 'auth'