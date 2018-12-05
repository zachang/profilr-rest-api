from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    """Allows users to edit profile"""

    def has_object_permission(self, request, view, obj):
        """Check if user is trying to edit profile"""

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id

class PostOwnStatus(permissions.BasePermission):
    """Allow users update their profile"""

    def has_object_permission(self, request, view, obj):
        """Check if user is trying to udpdate their status"""

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id