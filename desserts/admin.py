# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from desserts import models
import nested_admin

User = get_user_model()


class CartItemInline(nested_admin.NestedTabularInline):
    model = models.CartItem
    extra = 0


class OrderDessertInline(nested_admin.NestedTabularInline):
    model = models.OrderDessert
    extra = 0


class OrderResource(nested_admin.NestedModelAdmin):
    inlines = [OrderDessertInline]


class OrderInline(nested_admin.NestedTabularInline):
    model = models.Order
    inlines = [OrderDessertInline]
    extra = 0


class WhishlistInline(nested_admin.NestedTabularInline):
    model = models.Wishlist
    extra = 0


class DihlabUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class DihlabUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User


class UserResource(nested_admin.NestedModelAdmin, UserAdmin):
    form = DihlabUserChangeForm
    add_form = DihlabUserCreationForm
    fieldsets = UserAdmin.fieldsets
    inlines = [CartItemInline, OrderInline, WhishlistInline]


admin.site.register(User, UserResource)
admin.site.register(models.Dessert)
admin.site.register(models.Order, OrderResource)
admin.site.register(models.Wishlist)

admin.site.site_header = ugettext_lazy('AdRelated Dashboard')
admin.site.index_title = ugettext_lazy('Desserts Administration')
admin.site.site_header = ugettext_lazy('Dihlab')
admin.site.site_title = ugettext_lazy('Dihlab')
