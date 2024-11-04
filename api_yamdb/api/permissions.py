from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrAllowGet(BasePermission):
    """Разрешение для админа или GET-запроса."""

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )


class IsAdminIsSuperuser(BasePermission):
    """Разрешение для админа или суперюзера."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


class IsAuthorOrSuperUserOrReadOnly(BasePermission):
    """Разрешение для автора, админа и модератора."""

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user
                or request.user.is_admin
                or request.user.is_moderator
                )
