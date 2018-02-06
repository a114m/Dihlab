from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
# from django.contrib import admin
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework import routers
from desserts import apis


router = routers.DefaultRouter()
# router.register(r'users', apis.UserList)
router.register(r'desserts', apis.DessertViewSet)
# router.register(r'orders', apis.OrderViewSet)
router.register(r'wishlists', apis.WishlistViewSet)
router.register(r'cart', apis.OwnCartViewSet)
router.register(r'orders', apis.OrderViewSet)
router.register(r'orderdessert', apis.OrderDessertViewSet)

V1_BASE_URL = r'^api/v1/'

urlpatterns = [
    url(V1_BASE_URL, include(router.urls)),
    # url(r'^admin/', admin.site.urls),
    url(V1_BASE_URL + r'users/$', apis.UserList.as_view()),
    # url(V1_BASE_URL + r'users/(?P<pk>[0-9]+)/$', apis.UserDtail.as_view()),
    # url(V1_BASE_URL + r'orders/$', apis.OrderList.as_view()),
    # url(V1_BASE_URL + r'cart/checkout$', apis.CheckoutCart.as_view()),
    url(V1_BASE_URL + r'cart/checkout(/?$)?(/(?P<pk>[0-9]+))?/?$', apis.CheckoutCart.as_view()),
    url(V1_BASE_URL + r'cart/share/(?P<pk>[0-9]+)?/?$', apis.ShareCart.as_view()),

    # Authentication end-points
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^auth/', include('rest_auth.urls')),
    url(r'^auth/token-refresh/', refresh_jwt_token),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
