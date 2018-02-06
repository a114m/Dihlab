# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    cart_shared_with = models.ManyToManyField('self', symmetrical=False, related_name='shared_carts')
    is_guest = models.BooleanField('Guest', default=False, blank=True, help_text='Gust account? default is false')
    cart_items = models.ManyToManyField(
        'Dessert',
        through='CartItem',
        through_fields=('owner', 'dessert'),
        help_text='Items this user has in the cart',
    )


class Dessert(BaseModel):
    name = models.CharField(max_length=50, help_text='Shown name')
    price = models.DecimalField(max_digits=9, decimal_places=2, help_text='Dessert price')
    description = models.CharField(max_length=500, blank=True, help_text='Dessert description. [Optional]')
    image = models.ImageField(upload_to='desserts/', help_text='Shown image')
    calories = models.IntegerField(help_text='Number of calories the dessert provides')

    def __unicode__(self):
        return self.name


class CartItem(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, help_text='The user has the item on own cart')
    dessert = models.ForeignKey(Dessert, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, blank=False, null=False, help_text='Number of unit')

    def __unicode__(self):
        return "%x %s" % (self.quantity, self.dessert.name)


class Order(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    desserts = models.ManyToManyField(
        Dessert,
        through='OrderDessert',
        through_fields=('order', 'dessert'),
    )
    shared_with = models.ManyToManyField(User, related_name='shared_orders')

    def __unicode__(self):
        return "%s: %s's order" % (self.id, self.owner.username)


class OrderDessert(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    dessert = models.ForeignKey(Dessert, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, blank=False, null=False)

    def __unicode__(self):
        return "%sx %s" % (self.quantity, self.dessert.name)


class Wishlist(BaseModel):
    name = models.CharField(max_length=50, default='Untitled')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    desserts = models.ManyToManyField(Dessert)
    shared_with = models.ManyToManyField(User, related_name='shared_lists')

    def __unicode__(self):
        return "%s' %s wishlist" % (self.owner.username, self.name)
