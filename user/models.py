from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    birthdate = models.DateField()
    password = models.CharField(max_length=100)
    can_be_contacted = models.CharField(
        max_length=3, choices=[("yes", "Yes"), ("no", "No")], default="yes"
    )
    can_data_be_shared = models.CharField(
        max_length=3, choices=[("yes", "Yes"), ("no", "No")], default="yes"
    )

    def __str__(self):
        return self.username
