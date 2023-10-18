import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
from accounts.managers import UserManager



import random


def create_new_ref_number():
    not_unique = True
    while not_unique:
        unique_ref = random.randint(10_000, 99_999)
        if not User.objects.filter(device_id=unique_ref):
            not_unique = False
    return str(unique_ref)


class User(AbstractUser):

    objects = UserManager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)

    ip = models.CharField(max_length=50)

    mat = models.CharField(max_length=6, unique=True)
    name = models.CharField(max_length=6, unique=True, null=True, blank=True)

    device_id = models.CharField(max_length=40, unique=True, default=create_new_ref_number)
    user_agent = models.CharField(max_length=255)

    REQUIRED_FIELDS = ["ip", "user_agent", "mat"]

    def __str__(self):
        return "{} {}".format(self.username, self.ip)


