from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    """
    Custom user model manager where email or phone is the unique identifier
    for authentication instead of usernames.
    """

    def create_user(self, username,  ip, mat, user_agent, **extra_fields):

        if not username or not user_agent or not mat:
            raise ValueError(_("Users must have "))

        user = self.model(username=username, mat=mat, ip=ip, user_agent=user_agent, **extra_fields)
        user.save()

        user.password = user.device_id
        user.save()

        return user


    def create_user_by_email(self, email, password, **extra_fields):
        """
        :param email: user's email
        :param password:
        :param extra_fields: other's fields
        :return: user
        :rtype: User
        """

        if not email:
            raise ValueError(_("Users must have an email address"))

        if not password:
            raise ValueError(_("Users must have a password"))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.username = email
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user_by_email(username, password, **extra_fields)


