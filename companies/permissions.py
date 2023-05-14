from rest_framework import permissions


class CompanyPermission(permissions.BasePermission):
    message = "You should be company admin to perform this action."

    def has_permission(self, request, view):
        return request.user.is_admin() or view.action == "retrieve"
