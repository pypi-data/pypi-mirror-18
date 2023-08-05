from django.conf import settings
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject

from .util import get_user_agent


class DJMiddleware(MiddlewareMixin):
    # A middleware that adds a "user_agent" object to request
    def process_request(self, request):
        # It is use for find user agent and add in request
        request.user_agent = SimpleLazyObject(lambda: get_user_agent(request))

        ADMIN_LANGUAGE = 'en'
        ADMIN_HEADER_TITLE = "Django administrator"
        ADMIN_COLOR_THEME = "cyan"
        ALLOW_FORGET_PASSWORD_ADMIN = False
        # Add language for django admin
        if hasattr(settings, 'ALLOW_FORGET_PASSWORD_ADMIN'):
            ALLOW_FORGET_PASSWORD_ADMIN = settings.ALLOW_FORGET_PASSWORD_ADMIN

        if hasattr(settings, 'ADMIN_COLOR_THEME'):
            ADMIN_COLOR_THEME = settings.ADMIN_COLOR_THEME

        if hasattr(settings, 'ADMIN_LANGUAGE'):
            ADMIN_LANGUAGE = settings.ADMIN_LANGUAGE

        if hasattr(settings, 'ADMIN_HEADER_TITLE'):
            ADMIN_HEADER_TITLE = settings.ADMIN_HEADER_TITLE

        translation.activate(ADMIN_LANGUAGE)
        request.LANGUAGE_CODE = translation.get_language()
        request.ADMIN_HEADER_TITLE = ADMIN_HEADER_TITLE
        request.ADMIN_COLOR_THEME = ADMIN_COLOR_THEME
        request.ALLOW_FORGET_PASSWORD_ADMIN = ALLOW_FORGET_PASSWORD_ADMIN
