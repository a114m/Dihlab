from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
# from django.contrib import admin
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework import routers
from desserts import apis


router = routers.DefaultRouter()
router.register(r'users', apis.UserViewSet)
router.register(r'groups', apis.GroupViewSet)
router.register(r'desserts', apis.DessertViewSet)
router.register(r'orders', apis.OrderViewSet)
router.register(r'wishlists', apis.WishlistViewSet)


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/v1/', include(router.urls)),
    url(r'^auth/', include('rest_auth.urls')),
    url(r'^auth/token-refresh/', refresh_jwt_token),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
