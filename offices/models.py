from django.db import models


class Office(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=150)

    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE, related_name="offices")

    def __str__(self):
        return self.name
