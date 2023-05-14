from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User
from companies.models import Company
from companies.serializers import CompanySerializer
from offices.models import Office


class UserSerializer(serializers.HyperlinkedModelSerializer):
    office = serializers.PrimaryKeyRelatedField(queryset=Office.objects.all(), required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'office']

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        current_user = self.context.get("request").user

        user = User.objects.create(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            company=current_user.company,
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

    def update(self, instance, validated_data):
        for attr in ['first_name', 'last_name', 'office']:
            val = validated_data.get(attr, getattr(instance, attr))
            setattr(instance, attr, val)

        if validated_data.get('password'):
            instance.set_password(validated_data['password'])

        instance.save()

        return instance


class RegisterSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('password', 'email', 'first_name', 'last_name', 'company')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def create(self, validated_data):
        company_data = validated_data.pop('company')

        company = Company.objects.create(**company_data)

        user = User.objects.create(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            company=company
        )

        user.set_password(validated_data['password'])
        user.save()

        company.admin = user
        company.save()

        return user
