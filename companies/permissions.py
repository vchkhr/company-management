from rest_framework import permissions


class IsCompanyAdminPermission(permissions.BasePermission):
    message = 'You should be company admin to perform this action.'

    def has_permission(self, request, view):
        return request.method == "GET" or request.user.is_admin()
