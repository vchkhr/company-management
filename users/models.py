from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE, null=True, related_name='+')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def is_admin(self):
        return self == self.company.user
