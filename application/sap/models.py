from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from application.sap.managers import UserManager


class User(AbstractUser):
    registration_date = models.DateTimeField(
        default=timezone.now, 
        verbose_name="User's Registration Date"
    )
    rating = models.IntegerField(default=0, verbose_name="User's Rating")
    upload = models.ImageField(
        default="default/default_avatar.png", 
        upload_to="uploads/%Y/%m/%d/", 
        verbose_name="User's Avatar"
    )

    objects = UserManager()

    def __str__(self):
        return self.username


