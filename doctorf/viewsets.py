# Django REST Framework
from rest_framework import viewsets

# DRF-Extensions
from rest_framework_extensions.mixins import NestedViewSetMixin

# Doctor F
from .mixins import DetailSerializerDefaultMixin, RawDataFormMixin, MessagesMixin

__all__ = ['ReadOnlyModelViewSet', 'ModelViewSet']


class ReadOnlyModelViewSet(DetailSerializerDefaultMixin, NestedViewSetMixin, RawDataFormMixin, MessagesMixin, viewsets.ReadOnlyModelViewSet):
    pass


class ModelViewSet(DetailSerializerDefaultMixin, NestedViewSetMixin, RawDataFormMixin, MessagesMixin, viewsets.ModelViewSet):
    pass
