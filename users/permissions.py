from rest_framework import permissions

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']

class IsOwnerOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    This custom permission will only allow owners of
    object to edit and view OR
    allow to set methods
    """
    def has_object_permission(self, request, view, obj):
        if(request.method in SAFE_METHODS or obj == request.user):
            return True
        else:
            return False
class IsOwner(permissions.BasePermission):
    """
    This custom permission will only allow owners of
    object to edit and view OR
    allow to set methods
    """
    def has_object_permission(self, request, view, obj):
        if obj == request.user:
            return True
        else:
            return False

class IsOwnerObj(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsChatOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.chat.user == request.user
class IsChatPkOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        try:
            pk = request.resolver_match.kwargs.get('pk')
            return (request.user and request.user.is_authenticated) and request.user.chat_set.get(department__pk = pk)
        except:
            return False
