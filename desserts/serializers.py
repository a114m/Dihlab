"""Serializers define the API representation."""

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from desserts.models import Dessert, Order, Wishlist
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_guest',)


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name',)


class DessertSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dessert
        fields = ('url', 'name', 'description', 'image', 'calories',)


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ('url', 'owner', 'desserts', 'shared_with',)


class WishlistSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Wishlist
        fields = ('url', 'name', 'owner', 'desserts', 'shared_with',)
