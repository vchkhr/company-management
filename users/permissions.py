from rest_framework import permissions

from .models import User
from offices.models import Office


class UserPermission(permissions.BasePermission):
    message = "You should be company admin to perform this action."

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if view.action == "retrieve" or view.action == "partial_update":
            return request.user.is_admin() or str(request.user.id) == view.kwargs.get("pk")
        else:
            return request.user.is_admin()

        if request.data.get("office") and Office.objects.get(pk=request.data["office"]).company.admin != request.user:
            return False


class CompanyPermission(permissions.BasePermission):
    message = "You should be company admin to perform this action."

    def has_permission(self, request, view):
        return request.user.is_admin() or view.action == "retrieve"


class OfficePermission(permissions.BasePermission):
    message = "You should be company admin to perform this action."

    def has_permission(self, request, view):
        return request.user.is_admin() or (request.method == "GET" and view.kwargs.get("pk") is None)


class VehiclePermission(permissions.BasePermission):
    message = "You should be company admin to perform this action."

    def has_permission(self, request, view):
        return request.user.is_admin()
