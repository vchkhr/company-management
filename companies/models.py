from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=150, null=True)

    admin = models.ForeignKey("users.User", on_delete=models.CASCADE, null=True, related_name="+")

    def __str__(self):
        return self.name
