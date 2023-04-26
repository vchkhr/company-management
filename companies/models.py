from django.db import models
from users.models import User


class Company(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=150, null=True)

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, related_name='+')

    def __str__(self):
        return self.name

    def users(self):
        return User.objects.filter(company=self)


# class Office(models.Model):
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)


# class Vehicle(models.Model):
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
