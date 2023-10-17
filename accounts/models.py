import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
from accounts.managers import UserManager


class User(AbstractUser):

    objects = UserManager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    ip = models.CharField(max_length=50)

    username = models.CharField(max_length=6, unique=True)
    mat = models.CharField(max_length=6, unique=True)
    name = models.CharField(max_length=6, unique=True, null=True, blank=True)

    device_id = models.CharField(max_length=40, unique=True)

    user_agent = models.CharField(max_length=255)

    REQUIRED_FIELDS = ["ip", "user_agent", "mat", "device_id"]

    def __str__(self):
        return "{} {}".format(self.username, self.ip)

