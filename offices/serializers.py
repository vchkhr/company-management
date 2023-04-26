from rest_framework import serializers

from offices.models import Office


class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = ['name', 'country', 'region', 'city', 'address']

    def create(self, validated_data):
        current_user = self.context.get("request").user

        office = Office.objects.create(
            company=current_user.company,
            **validated_data
        )

        office.save()

        return office
