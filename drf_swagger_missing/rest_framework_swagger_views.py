from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.renderers import CoreJSONRenderer
from rest_framework_swagger.renderers import SwaggerUIRenderer

from drf_swagger_missing.rest_framework_swagger_renderers import BetterOpenAPIRenderer
from drf_swagger_missing.rest_framework_schemas import BetterSchemaGenerator


class SwaggerSchemaView(APIView):
    title = ''
    description = ''
    url = None
    patterns = None
    urlconf = None
    definitions = []
    version = ''
    check_view_permissions = True

    _ignore_model_permissions = True
    exclude_from_schema = True
    permission_classes = [AllowAny]
    renderer_classes = [
        CoreJSONRenderer,
        BetterOpenAPIRenderer,
        SwaggerUIRenderer
    ]

    def get(self, request):
        generator = BetterSchemaGenerator(
            title=self.title,
            url=self.url,
            description=self.description,
            patterns=self.patterns,
            urlconf=self.urlconf,
            definitions=self.definitions,
            version=self.version,
            check_view_permissions=self.check_view_permissions
        )
        schema = generator.get_schema(request=request)

        if not schema:
            raise exceptions.ValidationError(
                'The schema generator did not return a schema Document'
            )

        return Response(schema)
