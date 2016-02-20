# Django
from django.utils.module_loading import autodiscover_modules

# Django REST Framework
from rest_framework.routers import DefaultRouter

# DRF-Extensions
from rest_framework_extensions.routers import ExtendedDefaultRouter

__all__ = ['default_router']


class Router(ExtendedDefaultRouter):

    include_format_suffixes = False

    def get_api_root_view(self):
        self.registry.sort()
        return DefaultRouter.get_api_root_view(self)


def autodiscover():
    autodiscover_modules('routers')


default_router = Router()
