import os

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    def user_profile_avatar_path(self, instance):
        print("deleting file", self.avatar.delete)
        ext = instance.split(".")[-1]
        return "{0}/avatars/profile.{1}".format(self.username, ext)

    """Default user for rattletest."""

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    designation = models.CharField(max_length=255, blank=True)
    about_me = models.TextField(blank=True, null=True)
    avatar = models.ImageField(
        upload_to=user_profile_avatar_path, null=True, blank=True
    )
    website = models.URLField(blank=True, null=True)
    github_link = models.CharField(blank=True, null=True, max_length=50)
    twitter_link = models.CharField(blank=True, null=True, max_length=50)
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    mobile_number = models.CharField(
        validators=[phoneNumberRegex], max_length=16, unique=True, null=True, blank=True
    )
    address = models.CharField(blank=True, null=True, max_length=255)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    def filename(self):
        return os.path.basename(self.avatar.name)
