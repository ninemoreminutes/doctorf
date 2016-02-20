# Django REST Framework
from rest_framework import renderers


class BrowsableAPIRenderer(renderers.BrowsableAPIRenderer):
    '''
    Customizations to the default browsable API renderer for the raw data form.
    '''

    def get_context(self, data, accepted_media_type, renderer_context):
        # Store the associated response status to know how to populate the raw
        # data form.
        try:
            setattr(renderer_context['view'], '_raw_data_response_status', renderer_context['response'].status_code)
            return super(BrowsableAPIRenderer, self).get_context(data, accepted_media_type, renderer_context)
        finally:
            delattr(renderer_context['view'], '_raw_data_response_status')

    def get_raw_data_form(self, data, view, method, request):
        # Set a flag on the view to indiciate to the view/serializer that we're
        # creating a raw data form for the browsable API.  Store the original
        # request method to determine how to populate the raw data form.
        try:
            setattr(view, '_raw_data_form_marker', True)
            setattr(view, '_raw_data_request_method', request.method)
            return super(BrowsableAPIRenderer, self).get_raw_data_form(data, view, method, request)
        finally:
            delattr(view, '_raw_data_form_marker')
            delattr(view, '_raw_data_request_method')
