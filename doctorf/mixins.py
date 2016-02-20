# Python
import functools

# Django
from django.contrib import messages
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

# DRF-Extensions
from rest_framework_extensions.mixins import DetailSerializerMixin

__all__ = ['DetailSerializerDefaultMixin', 'RawDataFormMixin', 'MessagesMixin']


class DetailSerializerDefaultMixin(DetailSerializerMixin):

    def get_serializer_class(self):
        self.serializer_detail_class = self.serializer_detail_class or self.serializer_class
        return super(DetailSerializerDefaultMixin, self).get_serializer_class()


class RawDataFormMixin(object):

    def update_raw_data(self, data):
        # Use request data as-is when original request is an update and the
        # submitted data was rejected.
        request_method = getattr(self, '_raw_data_request_method', None)
        response_status = getattr(self, '_raw_data_response_status', 0)
        if request_method in ('POST', 'PUT', 'PATCH') and response_status in xrange(400, 500):
            return self.request.data.copy()
        return data

    def get_serializer(self, *args, **kwargs):
        serializer = super(RawDataFormMixin, self).get_serializer(*args, **kwargs)
        # Override when called from browsable API to generate raw data form;
        # update serializer "validated" data to be displayed by the raw data
        # form.
        if hasattr(self, '_raw_data_form_marker'):
            # Always remove read only fields from serializer.
            for name, field in serializer.fields.items():
                if getattr(field, 'read_only', None):
                    del serializer.fields[name]
            serializer._data = self.update_raw_data(serializer.data)
        return serializer


class MessagesMixin(object):

    def _get_instance_type(self, instance):
        return force_text(getattr(getattr(instance, '_meta', None), 'verbose_name', '')).capitalize()

    def _success_message(self, instance, suffix, instance_type=None):
        instance_type = instance_type or self._get_instance_type(instance)
        instance_text = force_text(instance)
        message = ' '.join(map(force_text, filter(None, [instance_type, instance_text, suffix])))
        messages.success(self.request._request, message)

    def perform_create(self, serializer):
        super(MessagesMixin, self).perform_create(serializer)
        self._success_message(serializer.instance, _('has been created.'))

    def perform_update(self, serializer):
        super(MessagesMixin, self).perform_update(serializer)
        self._success_message(serializer.instance, _('has been updated.'))

    def perform_destroy(self, instance):
        instance_type = self._get_instance_type(instance)
        instance_text = force_text(instance)
        super(MessagesMixin, self).perform_destroy(instance)
        self._success_message(instance_text, _('has been deleted.'), instance_type)

    def finalize_response(self, request, response, *args, **kwargs):
        response = super(MessagesMixin, self).finalize_response(request, response, *args, **kwargs)

        def clear_messages(func):
            @functools.wraps(func)
            def wrapper(*fargs, **fkwargs):
                result = func(*fargs, **fkwargs)
                list(messages.get_messages(request._request))
                return result
            return wrapper

        renderer = response.accepted_renderer
        renderer.render = clear_messages(renderer.render)
        return response
