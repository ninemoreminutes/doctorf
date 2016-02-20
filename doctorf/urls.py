# Django
from django.conf.urls import include, patterns, url

# Doctor F
from .routers import autodiscover, default_router


autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', include(default_router.urls, namespace='api')),
)
