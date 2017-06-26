import coreschema
from openapi_codec import encode
from rest_framework.schemas import OrderedDict


def _get_links(document):
    """
    This is an almost copy of openapi_codec.encode, here I generate tags from all the keys
    """
    links = []
    for keys, link in encode.get_links_from_document(document):
        if len(keys) > 1:
            operation_id = '_'.join(keys[1:])
            tags = keys  # here is the magic
        else:
            operation_id = keys[0]
            tags = []
        links.append((operation_id, link, tags))

    # Determine if the operation ids each have unique names or not.
    operation_ids = [item[0] for item in links]
    unique = len(set(operation_ids)) == len(links)

    # If the operation ids are not unique, then prefix them with the tag.
    if not unique:
        return [encode._add_tag_prefix(item) for item in links]

    return links

encode._get_links = _get_links


def _get_parameters(link, encoding):
    """
    body fields were hardcoded to {}, I'm using encode_schema
    parameter dict now get default value from field.schema.default
    """
    parameters = []
    properties = {}
    required = []

    for field in link.fields:
        location = encode.get_location(link, field)
        field_description = encode._get_field_description(field)
        field_type = encode._get_field_type(field)
        if location == 'form':
            if encoding in ('multipart/form-data', 'application/x-www-form-urlencoded'):
                # 'formData' in swagger MUST be one of these media types.
                parameter = {
                    'name': field.name,
                    'required': field.required,
                    'in': 'formData',
                    'description': field_description,
                    'type': field_type,
                }
                if field_type == 'array':
                    parameter['items'] = {'type': 'string'}
                parameters.append(parameter)
            else:
                # Expand coreapi fields with location='form' into a single swagger
                # parameter, with a schema containing multiple properties.

                schema_property = {
                    'description': field_description,
                    'type': field_type,
                }
                if field_type == 'array':
                    schema_property['items'] = {'type': 'string'}
                properties[field.name] = schema_property
                if field.required:
                    required.append(field.name)
        elif location == 'body':
            if encoding == 'application/octet-stream':
                # https://github.com/OAI/OpenAPI-Specification/issues/50#issuecomment-112063782
                schema = {'type': 'string', 'format': 'binary'}
            else:
                schema = encode_schema(field.schema)
            parameter = {
                'name': field.name,
                'required': field.required,
                'in': location,
                'description': field_description,
                'schema': schema
            }
            parameters.append(parameter)
        else:
            parameter = {
                'name': field.name,
                'required': field.required,
                'in': location,
                'description': field_description,
                'type': field_type or 'string',
                'default': field.schema.default,
            }
            if field_type == 'array':
                parameter['items'] = {'type': 'string'}
            parameters.append(parameter)

    if properties:
        parameter = {
            'name': 'data',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': properties
            }
        }
        if required:
            parameter['schema']['required'] = required
        parameters.append(parameter)

    return parameters
encode._get_parameters = _get_parameters


def _get_field_type(field):
    """My version supports the File type"""
    if getattr(field, 'type', None) is not None:
        # Deprecated
        return field.type

    if field.schema is None:
        return 'string'

    return _get_schema_type(field.schema)

encode._get_field_type = _get_field_type


def _get_schema_type(schema):
    """
    :type schema: coreschema.schemas.Schema
    """
    return {
        coreschema.String: 'string',
        coreschema.Integer: 'integer',
        coreschema.Number: 'number',
        coreschema.Boolean: 'boolean',
        coreschema.Array: 'array',
        coreschema.Object: 'object',
        coreschema.File: 'file',
    }.get(schema.__class__, 'string')


def _get_responses(link):
    """
    Returns minimally acceptable responses object based
    on action / method type if responses are not defined in the view.
    """
    if hasattr(link, '_responses'):
        responses = OrderedDict()
        for s, r in link._responses.items():
            responses[r.status] = encode_response(r)
        return responses
    template = {'description': ''}
    if link.action.lower() == 'post':
        return {'201': template}
    if link.action.lower() == 'delete':
        return {'204': template}
    return {'200': template}

encode._get_responses = _get_responses


def encode_schemas(schemas):
    """
    :type schemas: OrderedDict
    """
    definitions_dict = OrderedDict()
    for k, s in schemas.items():
        definitions_dict[s.title] = encode_schema(s)
    return definitions_dict


def encode_schema(schema):
    """A primitive, array or object
    :type schema: coreschema.schemas.Schema
    """
    entries = ('description', 'default', 'required', 'format')
    if isinstance(schema, coreschema.Ref):
        schema_dict = {'$ref': '#/definitions/%s' % schema.ref_name}
    else:
        schema_dict = {'type': _get_schema_type(schema)}
    for e in entries:
        value = getattr(schema, e, None)
        if value:
            schema_dict[e] = value
    properties = getattr(schema, 'properties', None)
    if properties:
        schema_dict['properties'] = encode_schemas(properties)

    if hasattr(schema, 'additional_properties') and schema.additional_properties:
        schema_dict['additionalProperties'] = encode_schema(schema.additional_properties_schema)

    if isinstance(schema, coreschema.Array):
        # Array has required field 'items'
        schema_dict['items'] = encode_schema(schema.items)
    return schema_dict


def encode_response(response):
    """
    todo: support headers and examples
    :type response: coreschema.Response
    """
    response_dict = OrderedDict()
    description = getattr(response, 'description', None)
    if description:
        response_dict['description'] = description
    schema = getattr(response, 'schema', None)
    if schema:
        response_dict['schema'] = encode_schema(schema)
    return response_dict


def _get_field_description(field):
    """Because Ref doesn't have description"""
    if getattr(field, 'description', None) is not None:
        # Deprecated
        return field.description

    if field.schema is None:
        return ''

    return getattr(field.schema, 'description', '')

encode._get_field_description = _get_field_description
