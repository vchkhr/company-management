from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True, related_name='+')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Company(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=150, null=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, related_name='+')

    def __str__(self):
        return self.name



# class Office(models.Model):
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)


# class Vehicle(models.Model):
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
