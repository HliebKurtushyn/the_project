from django.db import models
from django.contrib.auth.models import AbstractUser


# WIP
class CustomUser(AbstractUser):
    delivery_address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username
