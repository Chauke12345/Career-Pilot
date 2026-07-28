from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )


    full_name = models.CharField(
        max_length=200,
        blank=True
    )


    location = models.CharField(
        max_length=200,
        blank=True
    )


    linkedin = models.URLField(
        blank=True
    )


    github = models.URLField(
        blank=True
    )


    portfolio = models.URLField(
        blank=True
    )


    skills = models.TextField(
        blank=True,
        help_text="Comma separated skills"
    )


    bio = models.TextField(
        blank=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    updated_at = models.DateTimeField(
        auto_now=True
    )


    def __str__(self):

        return self.user.username