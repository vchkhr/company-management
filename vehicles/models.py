import datetime
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator


class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=20)
    year_of_manufacture = models.IntegerField(
        validators=[
            MaxValueValidator(datetime.date.today().year),
            MinValueValidator(datetime.date.today().year - 100)
        ]
    )

    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='vehicles')
    office = models.ForeignKey('offices.Office', on_delete=models.CASCADE, null=True, blank=True, related_name='vehicles')
    driver = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, blank=True, related_name='vehicles')

    def __str__(self):
        return self.name

    def clean(self):
        if self.office and len(self.company.office_set.all().filter(pk=self.office.id)) == 0:
            raise ValidationError({"office": "Not found."})

        if self.office and self.driver and self.driver.office != self.office:
            raise ValidationError({"driver": "Driver should be in the same office."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
