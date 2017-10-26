from drf_swagger_missing import coreschema
from drf_swagger_missing.rest_framework_swagger_views import SwaggerSchemaView


class MySwaggerView(SwaggerSchemaView):
    title = 'The title for the API'
    description = 'The description goes here'
    version = '1.0.0'

    # By default the schema generator will check if the current requesting user has permission for each view,
    # you may skip this check and present all your API paths to all users, including anonymous
    check_view_permissions = False

    # Extra object definitions
    definitions = [
        coreschema.Object(title='Store', properties=[
            coreschema.String(title='name', description='the store name'),
            coreschema.Object(title='metadata', description='Some kind of undefined object'),
            coreschema.Object(title='bands', description='One may add additional properties',
                              additional_properties=coreschema.Number()),
            coreschema.String(title='timestamp', format='date-time', description='the timestamp'),
            coreschema.Array(title='results', items=coreschema.Ref('bulk_result')),
            coreschema.Integer(title='integer_field'),
            coreschema.Anything(title='anything_field', description='The satellites service supplier'),
            coreschema.Boolean(title='bool_field'),
            coreschema.Number(title='number_field'),
        ]),

        # One may override the generated definition for some serializer
        coreschema.File(title='PizzaImageSerializer_read'),
        coreschema.Object(title='bulk_result', properties=[
            coreschema.Number(title='errors', description='number of errors in operation'),
            coreschema.Number(title='erroneus_data'),
            coreschema.Number(title='success', description='number of success in operation'),
        ]),
    ]
