from rest_framework.schemas import SchemaGenerator, OrderedDict, insert_into


class BetterSchemaGenerator(SchemaGenerator):
    prefix = ''
    definitions = []
    check_view_permissions = True

    def __init__(self, title=None, url=None, description=None, patterns=None, urlconf=None,
                 definitions=None, version='', check_view_permissions=True):
        super().__init__(title, url, description, patterns, urlconf)
        self.definitions = definitions or []
        self.version = version
        self.check_view_permissions = check_view_permissions

    def get_schema(self, request=None, public=False):
        """Add the base path and definitions to the document"""
        schema = super().get_schema(request, public)
        schema._base_path = self.prefix
        schema._definitions = self.definitions
        schema._version = self.version
        return schema

    def get_filter_fields(self, path, method, view):
        """Hack to add extra fields"""
        fields = super().get_filter_fields(path, method, view)
        method_name = getattr(view, 'action', method.lower())
        try:
            fields += view.Meta.fields.get(method_name, [])
        except AttributeError:
            # The view doesn't have Meta, Meta doesn't have .fields
            pass
        return fields

    def get_link(self, path, method, view):
        link = super().get_link(path, method, view)
        method = method.lower()
        try:
            link._responses = view.Meta.responses[method]
        except (AttributeError, KeyError):
            # The view doesn't have Meta, Meta doesn't have .responses or responses doesn't have this method
            pass
        return link

    def get_links(self, request=None):
        """Almost copy of parent, here I use subpath to create the link and save the base path"""
        links = OrderedDict()

        # Generate (path, method, view) given (path, method, callback).
        paths = []
        view_endpoints = []
        for path, method, callback in self.endpoints:
            view = self.create_view(callback, method, request)
            if getattr(view, 'exclude_from_schema', False):
                continue
            path = self.coerce_path(path, method, view)
            paths.append(path)
            view_endpoints.append((path, method, view))

        # Only generate the path prefix for paths that will be included
        if not paths:
            return None
        self.prefix = self.determine_path_prefix(paths)

        for path, method, view in view_endpoints:
            if self.check_view_permissions and not self.has_view_permissions(path, method, view):
                continue
            subpath = path[len(self.prefix):]
            link = self.get_link(subpath, method, view)
            keys = self.get_keys(subpath, method, view)
            insert_into(links, keys, link)
        return links