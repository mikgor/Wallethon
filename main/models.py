from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from rules.contrib.models import RulesModel
from django_currentuser.db.models import CurrentUserField
from uuid import uuid4, UUID

from main.managers import CustomUserManager
from main.utils import formatted_date


class BaseModel(RulesModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_by = CurrentUserField(on_delete=models.SET_NULL, editable=False, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    @property
    def uuid(self) -> UUID:
        return self.id

    def formatted_date(self, field):
        return formatted_date(getattr(self, field))

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')
        abstract = True


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.email

