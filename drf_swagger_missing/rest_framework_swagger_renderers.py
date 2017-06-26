from rest_framework_swagger.renderers import OpenAPICodec, OpenAPIRenderer
from openapi_codec import generate_swagger_object
from coreapi.compat import force_bytes
import simplejson as json
import coreapi
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from django.conf import settings

from drf_swagger_missing.openapi_codec_encode import encode_schemas


class BetterOpenAPICodec(OpenAPICodec):
    def encode(self, document, extra=None, **options):
        if not isinstance(document, coreapi.Document):
            raise TypeError('Expected a `coreapi.Document` instance')

        data = generate_swagger_object(document)
        data['info']['version'] = document._version
        data['info']['description'] = document.description
        if isinstance(extra, dict):
            data.update(extra)
        else:
            raise TypeError('`extra` should be a `dict` instance')

        return force_bytes(json.dumps(data))


class BetterOpenAPIRenderer(OpenAPIRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        """This is almost the same as parent, only here I use my own OpenAPICodec, add definitions and base path"""
        if renderer_context['response'].status_code != status.HTTP_200_OK:
            return JSONRenderer().render(data)
        extra = self.get_customizations()
        extra['definitions'] = encode_schemas(data._definitions)

        # if the base path auto detection doesn't work well for you it may be overridden
        extra['basePath'] = getattr(settings, 'API_BASE_PATH', data._base_path)

        return BetterOpenAPICodec().encode(data, extra=extra)
