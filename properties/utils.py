from rest_framework import permissions


class MerchantAuth(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.is_blocked and request.user.is_merchant
