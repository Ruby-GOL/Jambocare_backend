from rest_framework import permissions

class IsOwnerProfile(permissions.BasePermission):
    message = {"errors": {"details": "Available only for the owner"}}

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True


class IsOwnerUser(permissions.BasePermission):
    message = {"errors": {"details": "Available only for the owner"}}

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True


class IsEmailConfirm(permissions.BasePermission):
    message = {"errors": {"details": "Available only for confirm User"}}

    def has_permission(self, request, view):
        if request.user.is_email_confirmed:
            return True
