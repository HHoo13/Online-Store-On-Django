from django.contrib.auth.models import User
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsStaffOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in ('GET',) or
            request.user and request.user.is_staff
        )


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(obj.User == request.user
                    )


class IsStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_staff
                    )
