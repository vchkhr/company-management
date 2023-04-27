from rest_framework import permissions

from offices.models import Office


class IsAdminPermission(permissions.BasePermission):
    message = 'You should be company admin to perform this action.'

    def has_permission(self, request, view):
        return request.user.is_admin()


class IsAdminOrSelfPermission(permissions.BasePermission):
    message = 'You should be company admin to perform this action.'

    def has_permission(self, request, view):
        if request.data.get('office') and Office.objects.get(pk=request.data['office']).company.admin != request.user:
            return False
        return request.user.is_admin() or str(request.user.id) == view.kwargs.get('pk')


class IsAdminOrGetPermission(permissions.BasePermission):
    message = 'You should be company admin to perform this action.'

    def has_permission(self, request, view):
        return request.user.is_admin() or request.method == "GET"



class IsAdminOrIndexPermission(permissions.BasePermission):
    message = 'You should be company admin to perform this action.'

    def has_permission(self, request, view):
        return request.user.is_admin() or (request.method == "GET" and view.kwargs.get('pk') is None)
