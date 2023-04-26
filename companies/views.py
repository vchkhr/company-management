from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from django_filters.rest_framework import DjangoFilterBackend



# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     permission_classes = [IsCompanyAdminPermission]
#     queryset = User.objects.all().order_by('date_joined')
#     serializer_class = UserSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['email', 'first_name', 'last_name']

#     def get_queryset(self, *args, **kwargs):
#         return self.queryset.filter(company=self.request.user.company)
