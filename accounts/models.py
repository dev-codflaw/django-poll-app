from django.contrib.auth.models import AbstractUser
from django.db import models
import random


def generate_username():
    return ''.join(random.choices('ABCDEFGHJKMNPQRSTUVWXYZ' + '23456789', k=6))

class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True, default=generate_username)
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    email = models.EmailField(max_length=50, null=False, blank=False, unique=True)
    email_confirmed = models.BooleanField(default=False)


    def __str__(self):
        return self.email
