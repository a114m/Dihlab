"""Serializers define the API representation."""

from django.contrib.auth import get_user_model
from desserts.models import Dessert, Order, OrderDessert, Wishlist, CartItem
from rest_framework import serializers, exceptions


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class DessertSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dessert
        fields = ('id', 'url', 'name', 'price', 'description', 'image', 'calories',)


class CartSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CartItem
        fields = ('quantity', 'dessert')
    dessert = DessertSerializer()


class CartItemSerializer(serializers.Serializer):
    dessert_id = serializers.IntegerField(required=True, write_only=True)
    quantity = serializers.IntegerField(default=1)
    dessert = DessertSerializer(read_only=True)


class CartItemsSerializer(serializers.Serializer):
    desserts = serializers.ListField(child=CartItemSerializer())

    def create(self, validated_data):
        """Add desserts to cart."""
        # Get current user
        user = self.context['request'].user

        # Get current car items
        current_cart = CartItem.objects.filter(owner=user)
        current_cart_items_ids = map(lambda item: item.dessert_id, current_cart)

        # List to prepare items in-memory for bulk save
        cart_items = list()

        for dessert_data in validated_data['desserts']:
            dessert_id = dessert_data['dessert_id']
            # Break and return 400 if a dessert already in cart
            if dessert_id in current_cart_items_ids:
                raise exceptions.ParseError(detail="Dessert (%s) alraedy exists in the cart" % dessert_id)
                return
            try:  # Check if item_id added to cart is valid dessert_id else return 400
                dessert = Dessert.objects.get(id=dessert_id)  # FIXME: Bulk query instead of looping
            except Dessert.DoesNotExist:
                raise exceptions.ParseError(detail="No such Dessert ID (%s)" % dessert_id)
                return

            # Create CartItem in memory and add to cart_items list
            quantity = dessert_data['quantity']
            cart_items.append(
                CartItem(owner=user, dessert=dessert, quantity=quantity)
            )

        # Bulk save cart_items to DB
        result = CartItem.objects.bulk_create(cart_items)

        # Merge recently added items with the current ones in 'shared_with'cart to resturn
        # response with all items in cart
        response = {'desserts': list(current_cart) + result}
        return response


class OrderDessertSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderDessert
        fields = ('quantity', 'dessert')

    dessert = DessertSerializer(many=False, read_only=True)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'created_at', 'url', 'orderdessert_set',)

    orderdessert_set = OrderDessertSerializer(many=True, read_only=True)


class WishlistSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Wishlist
        fields = ('id', 'url', 'name', 'owner', 'desserts', 'shared_with',)
