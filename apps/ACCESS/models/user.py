from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from apps.BASE.managers import UserManager
from apps.BASE.models import (
    BaseModel,
    MAX_CHAR_FIELD_LENGTH,
    DEFAULT_BLANK_NULLABLE_FIELD_CONFIG,
)
from apps.BASE.model_fields import SingleChoiceField





# Custom User Model
class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.CharField(
        max_length=150, unique=True, **DEFAULT_BLANK_NULLABLE_FIELD_CONFIG
    )
    identity = models.CharField(
        max_length=MAX_CHAR_FIELD_LENGTH, **DEFAULT_BLANK_NULLABLE_FIELD_CONFIG
    )
    phone_number = models.CharField(max_length=MAX_CHAR_FIELD_LENGTH,**DEFAULT_BLANK_NULLABLE_FIELD_CONFIG)

    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return f"{self.email}"
