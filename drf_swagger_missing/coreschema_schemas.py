from collections import OrderedDict

import coreschema


class SchemaResponse:
    def __init__(self, status, description=None, schema=None, headers=None, examples=None):
        """
        todo create headers object (http://swagger.io/specification/#headersObject) and
        examples object (http://swagger.io/specification/#exampleObject)
        :type status: int or str
        :type description: str
        :type schema: coreschema.schemas.Schema
        """
        self.status = status
        self.description = description
        self.schema = schema
        self.headers = headers
        self.examples = examples

if not hasattr(coreschema, 'Response'):
    coreschema.Response = SchemaResponse

if not hasattr(coreschema, 'File'):
    # eventually it will support file, for now we insert this to be able to document file types
    class File(coreschema.schemas.Schema):
        pass
    coreschema.File = File


class BetterObject(coreschema.Object):
    def __init__(self, properties=None, required=None, max_properties=None, min_properties=None,
                 pattern_properties=None, additional_properties=True, **kwargs):
        if isinstance(properties, list):
            properties = OrderedDict([(p.title, p) for p in properties])
        super().__init__(properties, required, max_properties, min_properties, pattern_properties,
                         additional_properties, **kwargs)
coreschema.Object = BetterObject
