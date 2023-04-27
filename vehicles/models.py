from django.db import models


class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=20)
    year_of_manufacture = models.IntegerField()

    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE, null=True, related_name='vehicles')
    office = models.ForeignKey('offices.Office', on_delete=models.CASCADE, null=True, related_name='vehicles')
    driver = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, related_name='vehicles')

    def __str__(self):
        return self.name
