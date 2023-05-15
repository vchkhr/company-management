import datetime
from rest_framework import serializers

from vehicles.models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'name', 'model', 'license_plate', 'year_of_manufacture', 'office', 'driver']

    def create(self, validated_data):
        print("!!!!!!!!!!!")
        current_user = self.context.get("request").user

        vehicle = Vehicle.objects.create(
                company=current_user.company,
                **validated_data
                )

        vehicle.save()

        return vehicle
