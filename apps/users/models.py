from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.


class Roles(models.TextChoices):
    ADMIN = "Admin"
    USER = "User"


class User(AbstractBaseUser):
    id = models.BigAutoField(primary_key=True, db_index=True)
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=6, choices=Roles, default="User")

    USERNAME_FIELD = 'email'

