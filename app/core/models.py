"""
Database models.
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password=None, **extrad_field):
        """Create, save and return user"""
        if not email:
            raise ValueError('User maust have an email address.')
        user = self.model(email=self.normalize_email(email), **extrad_field)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    user in the system.
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Set user manager
    objects = UserManager()

    # Override default username field
    USERNAME_FIELD = 'email'
