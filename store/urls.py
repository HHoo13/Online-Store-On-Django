from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import SimpleRouter
from api.views import ProductViewSet, CategoryViewSet, OrderViewSet

router = SimpleRouter()
router.register('product', ProductViewSet, basename='product')
router.register('category', CategoryViewSet, basename='category')
router.register('order', OrderViewSet, basename='order')
urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('accounts/', include('django.contrib.auth.urls')),
                  path('', include("api.urls")),
                  path('cart/', include("cart.urls")),
                  path("__debug__/", include("debug_toolbar.urls")),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += router.urls
