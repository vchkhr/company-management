import datetime
from rest_framework import serializers

from vehicles.models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'name', 'model', 'license_plate', 'year_of_manufacture', 'office', 'driver']

    def validate(self, attrs):
        if attrs.get('year_of_manufacture'):
            current_year = datetime.date.today().year
            year = attrs['year_of_manufacture']
            min_year = current_year - 100

            if year < min_year or year > current_year:
                text = "Current year should be in range from %s to %s."%(min_year, current_year)
                raise serializers.ValidationError({"year_of_manufacture": text})

        vehicle_id = self.context['view'].kwargs.get('pk')
        if vehicle_id and (attrs.get('office') or attrs.get('driver')):
            vehicle = Vehicle.objects.get(pk=vehicle_id)
            office = attrs.get('office', vehicle.office)
            driver = attrs.get('driver', vehicle.driver)
            if office != driver.office:
                raise serializers.ValidationError({"driver": "Driver should be in the same office as the vehicle."})

        return attrs
