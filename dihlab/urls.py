from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
# from django.contrib import admin
from rest_framework import routers
from desserts import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'desserts', views.DessertViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'wishlists', views.WishlistViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
