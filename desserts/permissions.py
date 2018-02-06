from rest_framework import permissions
from django.contrib.auth import get_user_model

User = get_user_model()


class CartCheckout(permissions.BasePermission):
    """"Whether the current user has permission to access the requested cart."""

    message = "You do not have the permission to checkout this cart."

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)

    def has_permission(self, request, view):
        current_user = request.user
        cart_user_id = request.parser_context['kwargs'].get('pk')
        if cart_user_id is None or cart_user_id == str(current_user.id):
            return True
        try:
            current_user.shared_carts.get(id=cart_user_id)
        except User.DoesNotExist:
            return False
        else:
            return True
