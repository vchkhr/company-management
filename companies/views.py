from rest_framework import viewsets

from companies.serializers import CompanySerializer
from companies.permissions import CompanyPermission


class CompanyViewSet(viewsets.ModelViewSet):
    permission_classes = [CompanyPermission]
    serializer_class = CompanySerializer

    def get_object(self):
        return self.request.user.company
