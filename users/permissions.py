from rest_framework import permissions


class IsAdminOrSelfPermission(permissions.BasePermission):
    message = 'You should be company admin to perform this action.'

    def has_permission(self, request, view):
        return request.user.is_admin() or str(request.user.id) == view.kwargs.get('pk')


class IsAdminOrGetPermission(permissions.BasePermission):
    message = 'You should be company admin to perform this action.'

    def has_permission(self, request, view):
        return request.user.is_admin() or request.method == "GET"



class IsAdminOrIndexPermission(permissions.BasePermission):
    message = 'You should be company admin to perform this action.'

    def has_permission(self, request, view):
        return request.user.is_admin() or (request.method == "GET" and view.kwargs.get('pk') == None)
