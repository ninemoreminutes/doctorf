# Django REST Framework
from rest_framework.fields import get_attribute
from rest_framework import serializers

# DRF-Extensions
from rest_framework_extensions.utils import compose_parent_pk_kwarg_name

__all__ = ['NestedHyperlinkedRelatedField', 'ParentLinkedIdentityField']


class NestedHyperlinkedRelatedField(serializers.HyperlinkedRelatedField):

    def __init__(self, view_name=None, **kwargs):
        self.lookup_fields = kwargs.pop('lookup_fields', [kwargs.pop('lookup_field', self.lookup_field)])
        self.lookup_url_kwargs = kwargs.pop('lookup_url_kwargs', filter(None, [kwargs.pop('lookup_url_kwarg', None)]) or self.lookup_fields)
        super(NestedHyperlinkedRelatedField, self).__init__(view_name, **kwargs)

    def use_pk_only_optimization(self):
        return self.lookup_fields == ['pk']

    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {}
        for lookup_field, lookup_url_kwarg in zip(self.lookup_fields, self.lookup_url_kwargs):
            lookup_value = view_kwargs[lookup_url_kwarg]
            lookup_kwargs[lookup_field] = lookup_value
        return self.get_queryset().get(**lookup_kwargs)

    def get_url(self, obj, view_name, request, format):
        if hasattr(obj, 'pk') and obj.pk is None:
            return None
        lookup_url_kwargs = {}
        for lookup_field, lookup_url_kwarg in zip(self.lookup_fields, self.lookup_url_kwargs):
            lookup_value = get_attribute(obj, lookup_field.replace('__', '.').split('.'))
            lookup_url_kwargs[lookup_url_kwarg] = lookup_value
        return self.reverse(view_name, kwargs=lookup_url_kwargs, request=request, format=format)


class ParentLinkedIdentityField(serializers.HyperlinkedIdentityField):

    def __init__(self, view_name=None, **kwargs):
        self.parent_lookup_field = kwargs.pop('parent_lookup_field')
        self.parent_lookup_url_kwarg = kwargs.pop('parent_lookup_url_kwarg', compose_parent_pk_kwarg_name(self.parent_lookup_field))
        super(ParentLinkedIdentityField, self).__init__(view_name, **kwargs)

    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {
            self.parent_lookup_field: view_kwargs[self.parent_lookup_url_kwarg],
            self.lookup_field: view_kwargs[self.lookup_url_kwarg]
        }
        return self.get_queryset().get(**lookup_kwargs)

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            self.parent_lookup_url_kwarg: get_attribute(obj, self.parent_lookup_field.replace('__', '.').split('.')),
            self.lookup_url_kwarg: get_attribute(obj, self.lookup_field.replace('__', '.').split('.')),
        }
        return self.reverse(view_name, kwargs=url_kwargs, request=request, format=format)
