from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics

from offices.models import Office
from offices.serializers import OfficeSerializer
from users.permissions import IsAdminOrIndexPermission


class OfficeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows offices to be viewed or edited.
    """
    permission_classes = [IsAdminOrIndexPermission]
    queryset = Office.objects.all().order_by('name')
    serializer_class = OfficeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['country', 'city']

    def get_object(self):
        return self.request.user.company


class OfficeRetrieveView(generics.RetrieveAPIView):
    queryset = Office.objects.all().order_by('name')
    serializer_class = OfficeSerializer

    def get_object(self):
        return self.request.user.office
