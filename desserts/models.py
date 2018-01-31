# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    cart_shared_with = models.ManyToManyField('self', symmetrical=False, related_name='shared_carts')
    is_guest = models.BooleanField('Guest', default=False, blank=True)
    cart_items = models.ManyToManyField(
        'Dessert',
        through='CartItem',
        through_fields=('owner', 'dessert'),
    )


class Dessert(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500, blank=True)
    image = models.ImageField(upload_to='dessert_imgs/')
    calories = models.IntegerField()

    def __unicode__(self):
        return self.name


class CartItem(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
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
