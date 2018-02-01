# -*- coding: utf-8 -*-
"""ViewSets define the view behavior."""

from __future__ import unicode_literals
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from desserts.models import Dessert, Order, Wishlist
from rest_framework import viewsets
from desserts import serializers

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """API endpoint that allows users to be viewed or edited."""

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """API endpoint that allows groups to be viewed or edited."""

    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer


class DessertViewSet(viewsets.ModelViewSet):
    """API endpoint that allows view and edit of desserts."""

    queryset = Dessert.objects.all()
    serializer_class = serializers.DessertSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """API endpoint that allows view and edit of orders."""

    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer


class WishlistViewSet(viewsets.ModelViewSet):
    """API endpoint that allows view and edit of wishlists."""

    queryset = Wishlist.objects.all()
    serializer_class = serializers.WishlistSerializer
