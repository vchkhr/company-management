from rest_framework import viewsets, generics

from vehicles.models import Vehicle
from vehicles.serializers import VehicleSerializer
from users.permissions import IsAdminPermission
from django_filters.rest_framework import DjangoFilterBackend


class VehicleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminPermission]
    queryset = Vehicle.objects.all().order_by('name')
    serializer_class = VehicleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['office', 'driver']

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(company=self.request.user.company)


class VehicleListView(generics.ListAPIView):
    queryset = Vehicle.objects.all().order_by('name')
    serializer_class = VehicleSerializer

    def get_queryset(self):
        return self.queryset.filter(driver=self.request.user)
