from rest_framework import permissions

from backend.models import User

class IsCompanyAdminPermission(permissions.BasePermission):
    message = 'You should be company admin to perform this action.'

    def has_permission(self, request, view):
        return str(request.user.id) == view.kwargs.get('pk') or request.user.is_admin()
