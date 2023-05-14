from django.db import models
from django.contrib.auth.models import AbstractUser

from django.core.exceptions import ValidationError


class User(AbstractUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)

    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='users')
    office = models.ForeignKey('offices.Office', on_delete=models.CASCADE, null=True, blank=True, related_name='users')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def is_admin(self):
        return self == self.company.admin

    def clean(self):
        if self.office is not None and self.office.company != self.company:
            raise ValidationError(
                {"office": _("Not found.")}
            )
