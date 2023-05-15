from rest_framework import serializers

from companies.models import Company
from offices.serializers import OfficeSerializer


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        # users = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
        fields = ['name', 'address']
