# DRF-swagger-missing
## Missing things to make a real world swagger for your DRF project

I wanted to generate a swagger file and stop editing the swagger.yml
manually, unfortunately there were too many missing things from the
various projects involved, I hope this project will die as soon as
possible and the features integrated in each project.

# Usage:

1. `pip install drf-swagger-missing`

2. Add `rest_framework_swagger` to your `INSTALLED_APPS` setting:
```python
    INSTALLED_APPS = (
        ...
        'rest_framework_swagger',
    )
```
    
3. Create your view and set the parameters you need
```python
class MySwaggerView(drf_swagger_missing.SwaggerSchemaView):
    title = 'My system REST API'
    description = 'This is a system that I made'
    version = '1.0.0'
    check_view_permissions = False

    definitions = [
        coreschema.Object(title='Scene', properties=[
            coreschema.String(title='scene_id', description='the scene id'),
            coreschema.Object(title='bands', description='A dictionary',
                              additional_properties=coreschema.Number()),
            coreschema.String(title='metadata_url', description='Url reference'),
            coreschema.String(title='timestamp', format='date-time', description='the timestamp'),
            coreschema.Array(title='rasters', items=coreschema.Ref('Raster')),
            coreschema.String(title='productname'),
            coreschema.Number(title='errors', description='number of errors in operation'),
        ]),
        coreschema.Object(title='Raster', properties=[
            coreschema.String(title='url', description='A URL'),
            coreschema.Array(title='bands', description='list of bands', items=coreschema.String()),
        ]),
    ]
```
    
4. Add your view to your urls.py
```python
urlpatterns = [
    url(r'^docs/$', MySwaggerView.as_view()),
    ...
]
```
 
5. Add responses and extra parameters to your views using Meta class for your CBV:
```python
class SceneView(APIView):
    class Meta:
        responses = {
            'get': [
                coreschema.Response(status=status.HTTP_200_OK, description='A Scene object',
                                    schema=coreschema.Ref('Scene')),
                coreschema.Response(status.HTTP_404_NOT_FOUND, description='Scene not found'),
                ],
            'post': [
                coreschema.Response(status.HTTP_200_OK, description='Result object',
                                    schema=coreschema.Object()),
                coreschema.Response(status.HTTP_404_NOT_FOUND, description='Scene not found'),
            ],
            'put': [
                coreschema.Response(status.HTTP_200_OK, description='The scene object', schema=coreschema.Ref('Scene')),
                coreschema.Response(status.HTTP_400_BAD_REQUEST),
                coreschema.Response(status.HTTP_404_NOT_FOUND, description='Scene not found'),
                coreschema.Response(status.HTTP_408_REQUEST_TIMEOUT),
            ],
            'delete': [
                coreschema.Response(status=status.HTTP_200_OK, description='The Scene object deleted',
                                    schema=coreschema.Ref('Scene')),
                coreschema.Response(status.HTTP_404_NOT_FOUND, description='Scene not found'),
            ]
        }
        fields = {
            'post': [
                coreapi.Field(name='scene_attributes', required=True, location='body',
                              schema=coreschema.Ref('Scene')),
            ],
            'put': [
                coreapi.Field(name='data', required=True, location='body',
                              schema=coreschema.Ref('Scene')),
            ]
        }
```


# What am I adding?

## openapi_codec.encode
1. _get_links
the original function just add the first key generated as tag, 
I changed the behaviour to add all keys as tags.
Maybe this could be merged as an optional bahaviour, one flag could be added

2. _get_parameters
schema for body fields is hardcoded to {}, using encode_schema instead of
hardcoded empty dict

parameter dict ignores default value, using field.schema.default

3. _get_field_type
uses _get_schema_type

3. _get_schema_type
created this, functionality was inside get_field_type
now it supports file type

4. _get_responses
returns encoded responses if present, else continues returning the
hardcoded values

4. encode_schemas
created to encode a schema list, useful for the definitions list

5. encode_schema
created to encode a coreschema.schemas.Schema object

6. encode_response
created to encode coreschema.Response, which doesn't exist yet,
I'm adding below

7. _get_field_description
using ```getattr(field.schema, 'description', '')``` because not all
all schema types have a description, eg: Ref

## rest_framework_swagger.renderers.OpenAPICodec

Add a BetterOpenAPICodec class which adds version and description to the document

## rest_framework_swagger.renderers.OpenAPIRenderer.render()
BetterOpenAPIRenderer class can add object definitions entries and document base path

## coreschema.schema

Response class
Field class

## rest_framework.schemas.SchemaGenerator

Adding prefix, definitions and check_view_permissions attributes to the class

### rest_framework.schemas.SchemaGenerator.get_schema()

adding base_path, definitions and version to the schema document

### rest_framework.schemas.SchemaGenerator.get_filter_fields()
Adding extra fields if they are defined in the view class as the example above
Ideally it should have a get_extra_fields function

Useful if for some reason some of your fields couldn't be
automatically detected
 
### rest_framework.schemas.SchemaGenerator.get_link()

adding responses list if they are defined on the Meta for the method,
see example above

### rest_framework.schemas.SchemaGenerator.get_links()

The common links prefix is already calculated, I save it so it may be
used as basePath on swagger

This behaviour to auto calculate should be a flag, also user should be able
to manual override the basePath

I also changed the line ```link = self.get_link(path, method, view)```
to use subpath instead of path ```link = self.get_link(subpath, method, view)```
 
## rest_framework_swagger SwaggerSchemaView

created SwaggerSchemaView to be used as a Base class with the attributes
one need to customize

## coreapi.Document
Adding base_path, definitions and version attributes
