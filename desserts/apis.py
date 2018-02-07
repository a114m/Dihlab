# -*- coding: utf-8 -*-
"""ViewSets define the view behavior."""

from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from desserts.models import Dessert, Order, OrderDessert, Wishlist, CartItem
from desserts import permissions as custom_permissions
from desserts import serializers
from rest_framework import viewsets, generics, views, exceptions, permissions, mixins
from rest_framework.response import Response

User = get_user_model()


class UserList(generics.ListAPIView):
    """
    API endpoint to list other users than the current user and admins.

    get:
    List all registered users ids (to use on sharing cart or access others)
    """

    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        """Filter guests and the current user."""
        user = self.request.user
        queryset = User.objects.all()\
            .order_by('username')\
            .filter(is_guest=False, is_staff=False)\
            .exclude(id=user.id)
        return queryset


class DessertViewSet(viewsets.ModelViewSet):
    """API endpoint that allows view and edit of desserts."""

    queryset = Dessert.objects.all()
    serializer_class = serializers.DessertSerializer

    def get_permissions(self):
        """
        Dessert permissions.

        Allow only admins to use unsafe methods on desserts (for create, update, delete, etc..).
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


class OwnCartViewSet(viewsets.ModelViewSet):
    """
    API endpoint to view and add desserts to cart.

    get:
    List own cart desserts

    post:
    Add dessert to own cart ex.:
    {
        "desserts": [
            {
                "dessert_id": 5,
                "quantity": 3
            }
        ]
    }
    """

    queryset = CartItem.objects.all()

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(owner=user)
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return serializers.CartItemsSerializer
        else:
            return serializers.CartSerializer


class ShareCart(views.APIView):
    """
    API endpoint to share/unshare cart with provided user_id.

    post:
    "/<user_id>" Share current user cart with user_id

    delete:
    "/<user_id>" Unshare current user cart with user_id
    will return 200 even if invalid user_id is provided or the cart wasn't shared
    """

    def _share_cart(self, user, share_with):
        user.cart_shared_with.add(share_with)
        return 'shared'

    def _unshare_cart(self, user, share_with):
        user.cart_shared_with.remove(share_with)
        return 'unshared'

    def post(self, request, *args, **kwargs):
        return self._apply_action(request, self._share_cart)

    def put(self, request, *args, **kwargs):
        return self._apply_action(request, self._share_cart)

    def delete(self, request, *args, **kwargs):
        return self._apply_action(request, self._unshare_cart)

    def _apply_action(self, request, action):
        user = request.user
        share_with_id = int(self.kwargs["pk"])
        if user.id == share_with_id:
            raise exceptions.ParseError(detail="You jackass trying to share cart with yourself")

        try:
            result = action(user, share_with_id)
        except IntegrityError:
            raise exceptions.ParseError(detail="Invalid user_id")
        except Exception as err:
            raise exceptions.APIException(detail="Something went wrong: %s" % err)
        else:
            return Response("Successfully %s cart with user (%s)" % (result, share_with_id))


class CheckoutCart(views.APIView):
    """
    API endpoint to checkout own cart or shared cart with you.

    post:
    "/" Checkout own cart
    "/user_id" Check the shared cart with you for user_id
    """

    permission_classes = (custom_permissions.CartCheckout,)

    def update(self, request, *args, **kwargs):
        user = request.user
        return self._checkout(user)

    def post(self, request, *args, **kwargs):
        user_id = self.kwargs.get("pk")

        # Get User instance to checkout her/his cart (current user if none else is sent in url)
        user = request.user if user_id is None else User.objects.get(id=user_id)

        return self._checkout(user)

    def _checkout(self, user):
        cart_items = CartItem.objects.filter(owner=user)
        order = Order.objects.create(owner=user)
        try:
            order_items = map(
                lambda item: OrderDessert(
                    order=order, quantity=item.quantity, dessert=item.dessert
                ), cart_items
            )
        except Exception as err:
            order.delete()
            raise exceptions.APIException(detail=err)
        try:
            OrderDessert.objects.bulk_create(order_items)
        except Exception as err:
            raise exceptions.APIException(detail=err)
        else:
            user.cart_items.clear()
            return Response("Cart Checked Out")


# class OrderViewSet(viewsets.ModelViewSet):
class OrderViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """API endpoint that allows list, view and delete of orders."""

    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = user.order_set.all()

        return queryset


class OrderDessertViewSet(viewsets.ModelViewSet):
    queryset = OrderDessert.objects.all()
    serializer_class = serializers.OrderDessertSerializer


class WishlistViewSet(viewsets.ModelViewSet):
    """API endpoint that allows view and edit of wishlists."""

    queryset = Wishlist.objects.all()
    serializer_class = serializers.WishlistSerializer
