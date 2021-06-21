from django.contrib import (
    admin,
)
from django.urls import (
    include,
    path,
    re_path,
)
from django.views.generic import (
    TemplateView,
)

from rest_framework.routers import (
    DefaultRouter,
)
from rest_framework.schemas import (
    get_schema_view,
)

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
)

from .social_network.views import (
    AnalyticsView,
    PostViewSet,
    UserViewSet,
    UserActivityView,
    SignUp,
)


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    re_path(r'^analytics/$', AnalyticsView.as_view()),
    path(
        'auth/',
        include('rest_framework.urls', namespace='rest_framework'),
    ),
    path(
        'auth/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair',
    ),
    path(
        'auth/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh',
    ),
    path(
        'user_activity/<int:pk>/',
        UserActivityView.as_view(),
        name='user_activity',
    ),
    path('sign_up/', SignUp.as_view(), name='sign_up'),
    path(
        'openapi/',
        get_schema_view(
            title='SocialNetworkAPI',
            description='API for all things',
            version='1.0',
        ),
        name='openapi-schema',
    ),
    path(
        'swagger-ui/',
        TemplateView.as_view(
            template_name='swagger-ui.html',
            extra_context={
                'schema_url': 'openapi-schema',
            },
        ),
        name='swagger-ui',
    ),
]
