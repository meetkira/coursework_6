from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from djoser.views import UserViewSet
from drf_spectacular.views import SpectacularAPIView

from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from ads.views import CommentViewSet, AdViewSet

router = SimpleRouter()

router.register("users", UserViewSet, basename="users")
router.register('ads', AdViewSet, basename="ads")
router.register(r'ads/(?P<ad_id>\d+)/comments', CommentViewSet, basename="comments")

urlpatterns = [
    path("api/admin/", admin.site.urls),
    path("api/redoc-tasks/", include("redoc.urls")),
    path("", include(router.urls)),
    path('api/auth/', include('djoser.urls')),
    path("api/auth/", include("djoser.urls.jwt")),
    path("token/", TokenObtainPairView.as_view(), name='token'),
    path("token/refresh/", TokenRefreshView.as_view(), name='refresh_token'),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
