from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.publisher.id, filename)

def user_directory_path_User(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'files/user_{0}/{1}'.format(instance.id, filename)

class UserPersonalized(AbstractUser):
    biography= models.TextField(max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to=user_directory_path_User, null=True, blank=True)
    website = models.TextField(max_length=255, null=True, blank=True, default='')
    gender = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)
    available = models.BooleanField(default=False)

    # Create your models here.