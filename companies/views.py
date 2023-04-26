from rest_framework import viewsets

from companies.serializers import CompanySerializer
from users.permissions import IsAdminOrGetPermission


class CompanyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrGetPermission]
    serializer_class = CompanySerializer

    def get_object(self):
        return self.request.user.company
