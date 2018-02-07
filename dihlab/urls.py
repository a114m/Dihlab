from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework import routers
from desserts import apis


V1_BASE_URL = r'^api/v1/'

router = routers.DefaultRouter()
router.register(r'desserts', apis.DessertViewSet)
router.register(r'cart', apis.OwnCartViewSet)
router.register(r'orders', apis.OrderViewSet)
router.register(r'orderdessert', apis.OrderDessertViewSet)
router.register(r'wishlists', apis.WishlistViewSet)


urlpatterns = [
    url(V1_BASE_URL, include(router.urls)),
    url(V1_BASE_URL + r'users/$', apis.UserList.as_view()),
    url(V1_BASE_URL + r'cart/checkout(/?$)?(/(?P<pk>[0-9]+))?/?$', apis.CheckoutCart.as_view()),
    url(V1_BASE_URL + r'cart/share/(?P<pk>[0-9]+)?/?$', apis.ShareCart.as_view()),

    # Authentication end-points
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^auth/', include('rest_auth.urls')),
    url(r'^auth/token-refresh/', refresh_jwt_token),
]

if settings.ENV == 'development':
    urlpatterns += [
        url(r'^admin/', admin.site.urls),
        url(r'^nested_admin/', include('nested_admin.urls')),
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
