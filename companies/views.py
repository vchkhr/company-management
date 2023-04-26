from rest_framework import viewsets, generics, permissions

from companies.models import Company
from companies.serializers import CompanySerializer
from companies.permissions import IsCompanyAdminPermission
from django_filters.rest_framework import DjangoFilterBackend


class CompanyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsCompanyAdminPermission]
    serializer_class = CompanySerializer

    def get_object(self):
        return self.request.user.company
