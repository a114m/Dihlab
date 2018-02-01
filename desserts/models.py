# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    cart_shared_with = models.ManyToManyField('self', symmetrical=False, related_name='shared_carts')
    is_guest = models.BooleanField('Guest', default=False, blank=True, help_text='Gust account? default is false')
    cart_items = models.ManyToManyField(
        'Dessert',
        through='CartItem',
        through_fields=('owner', 'dessert'),
        help_text='Items this user has in the cart',
    )


class Dessert(models.Model):
    name = models.CharField(max_length=50, help_text='Shown name')
    description = models.CharField(max_length=500, blank=True, help_text='Dessert description. [Optional]')
    image = models.ImageField(upload_to='desserts/', help_text='Shown image')
    calories = models.IntegerField(help_text='Number of calories the dessert provides')

    def __unicode__(self):
        return self.name


class CartItem(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, help_text='The user has the item on own cart')
    dessert = models.ForeignKey(Dessert, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False, null=False)

    def __unicode__(self):
        return "%s's cart item: %s" % (self.owner.username, self.dessert.name)


class Order(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    desserts = models.ManyToManyField(
        Dessert,
        through='OrderDessert',
        through_fields=('order', 'desert'),
    )
    shared_with = models.ManyToManyField(User, related_name='shared_orders')

    def __unicode__(self):
        return "%s: %s's order" % (self.id, self.owner.username)


class OrderDessert(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    desert = models.ForeignKey(Dessert, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False, null=False)

    def __unicode__(self):
        return "%sx %s" % (self.quantity, self.desert.name)


class Wishlist(models.Model):
    name = models.CharField(max_length=50, default='Untitled')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    desserts = models.ManyToManyField(Dessert)
    shared_with = models.ManyToManyField(User, related_name='shared_lists')

    def __unicode__(self):
        return "%s' %s wishlist" % (self.owner.username, self.name)
