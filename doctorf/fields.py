# Django REST Framework
from rest_framework.reverse import reverse
from rest_framework import serializers

# DRF-Extensions
from rest_framework_extensions.utils import compose_parent_pk_kwarg_name

__all__ = ['ParentLinkedIdentityField']


class ParentLinkedIdentityField(serializers.HyperlinkedIdentityField):

    def __init__(self, view_name=None, **kwargs):
        self.parent_lookup_field = kwargs.pop('parent_lookup_field')
        self.parent_lookup_url_kwarg = kwargs.pop('parent_lookup_url_kwarg', compose_parent_pk_kwarg_name(self.parent_lookup_field))
        super(ParentLinkedIdentityField, self).__init__(view_name, **kwargs)

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            self.parent_lookup_url_kwarg: getattr(obj, self.parent_lookup_field),
            self.lookup_url_kwarg: getattr(obj, self.lookup_field),
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {
            self.parent_lookup_field: view_kwargs[self.parent_lookup_url_kwarg],
            self.lookup_field: view_kwargs[self.lookup_url_kwarg]
        }
        return self.get_queryset().get(**lookup_kwargs)
