from rest_framework import viewsets, generics, permissions

from users.models import User
from users.serializers import UserSerializer, RegisterSerializer
from users.permissions import UserPermission
from django_filters.rest_framework import DjangoFilterBackend


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = [UserPermission]
    queryset = User.objects.all().order_by('date_joined')
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['email', 'first_name', 'last_name']

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(company=self.request.user.company)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
