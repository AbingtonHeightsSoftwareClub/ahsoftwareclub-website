from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

class User(AbstractBaseUser):
    is_trailing = models.BooleanField(default=True)
    # add extra fields here