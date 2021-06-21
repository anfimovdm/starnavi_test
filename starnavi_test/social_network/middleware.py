from django.utils import timezone

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_302_FOUND,
)
from rest_framework_simplejwt.tokens import (
    AccessToken,
)

from .models import (
    UserProfile,
)


LOGIN_PATHS = (
    '/auth/login/',
    '/auth/token/',
    '/auth/token/refresh',
    '/sign_up/',
)
HTTP_STATUSES = (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_302_FOUND,
)


class UpdateLastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        user_id = request.user.id
        request_auth = getattr(request, 'auth', None)
        if request_auth is not None:
            user_id = request.auth.get('user_id')

        model_params = {
            'last_request': timezone.now(),
        }
        if response.status_code in HTTP_STATUSES and (
                request.path in LOGIN_PATHS):
            model_params.update({
                'last_login': timezone.now(),
            })
            if user_id is None and getattr(response, 'data', None) is not None:
                token = response.data.get('access') or response.data.get('token')
                if isinstance(token, dict):
                    token = token.get('access')
                user_id = AccessToken(
                    token=token,
                ).get('user_id')

        if user_id is not None:
            UserProfile.objects.update_or_create(
                user_id=user_id,
                defaults=model_params,
            )
        return response
