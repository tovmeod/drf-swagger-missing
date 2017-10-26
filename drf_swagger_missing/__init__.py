import coreschema  # noqa
import drf_swagger_missing.coreapi_document
import drf_swagger_missing.coreschema_schemas
import drf_swagger_missing.openapi_codec_encode
import drf_swagger_missing.rest_framework_swagger_renderers
import drf_swagger_missing.rest_framework_swagger_views
import drf_swagger_missing.rest_framework_schemas
import drf_swagger_missing.rest_framework_schemas_inspector  # noqa

# todo: print warning about unused response defined in Meta, for unexisting action
# todo: meta.fields should be stored as OrderedDict, user should be able to overwrite detected fields
# todo: user should be able to overwrite detected definitions
# todo: http://editor.swagger.io complains
# todo: meta responses and fields could be decorators
# todo: parameters of type file must include 'multipart/form-data' in their 'consumes' property
