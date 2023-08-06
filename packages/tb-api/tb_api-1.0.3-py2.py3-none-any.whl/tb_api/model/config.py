from __future__ import print_function

from os.path import abspath

from tb_api.router import PathRouter
from tb_api.utils.config_utils import parse_method_path


class Config(object):
    def __init__(self, project_dir, debug, port):
        self.debug = debug
        self.project_dir = abspath(project_dir)
        self.port = port
        self.loader = None

        # File to auto-reload when run in debug mode
        self.extra_files = []


class APIMethodConfig(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __getattr__(self, item):
        return self.kwargs.get(item)

    def get_field(self, name):
        return self.field_map.get(name)


class APIFieldConfig(object):
    def __init__(self, config):
        self.name = config['name']
        self.description = config.get('description', '')
        self.required = config.get('required', True)
        self.type = self._clean_type(config.get('type', 'string'))
        self.param_in = config.get('in', 'query')
        self.defaultValue = config.get('default')
        self.schema = config.get('schema')

    def set_field_type(self, flask_type):
        if flask_type == 'int':
            self.type = 'integer'
        elif flask_type == 'float':
            self.type = 'float'
        else:
            self.type = 'string'

    @staticmethod
    def _clean_type(param_type):
        if param_type == 'int':
            return 'integer'

        return param_type

    def parse_value(self, value):
        if self.type == 'integer':
            return int(value)
        elif self.type == 'float':
            return float(value)

        return value


class APIConfig(object):
    copy_fields = [
        ('summary', 'summary', None),
        ('description', 'description', None),
        ('method', 'http_methods', ['get']),
    ]

    path_copy_fields = [
        ('summary', 'summary', None),
        ('description', 'description', None),
        ('require', 'require', []),
        ('type', 'type', 'string'),
        ('deprecated', 'deprecated', None),
    ]

    def __init__(self, data):
        self.data = data

        self.path_router = PathRouter()

        self._build_services(data)
        self._build_paths(data)

    def get_config(self, method, url):
        return self.path_router.search(method, url)

    def _build_services(self, data):
        services = data.get('services', {})
        for module_name in services:
            module_config = services[module_name]
            module_path = module_config.get('path', module_name)
            # if module_path not in self.path_router:
            #     self.path_router[module_path] = {}

            methods = module_config.get('methods', {})
            tags = module_config.get('tags', [])
            require = module_config.get('require', [])

            for method_name in methods:
                method_config = methods[method_name]
                method_path = method_config.get('path', method_name)
                fields = [APIFieldConfig(_) for _ in method_config.get('fields', [])]
                method_tags = tags + method_config.get('tags', [])
                method_require = require + method_config.get('require', [])
                params = {
                    'module_name': module_name,
                    'method_name': method_name,
                    'fields': fields,
                    'tags': method_tags,
                    'require': method_require,
                }

                for field, param_field, default_value in self.copy_fields:
                    params[param_field] = method_config.get(field, default_value)

                method_config = APIMethodConfig(**params)

                if method_path is None:
                    path = '/%s' % module_path
                else:
                    path = '/%s/%s' % (module_path, method_path)

                for http_method in method_config.http_methods:
                    self.path_router.add_path(method=http_method, text=path, data=method_config)

    def _build_paths(self, data):
        paths = data.get('paths', {})
        for path_text in paths:
            path_config = paths[path_text]

            assert isinstance(path_config, dict)

            if not path_text.startswith('/'):
                path_text = '/%s' % path_text

            tags = path_config.get('tags', [])
            for http_method in PathRouter.support_methods:
                if http_method not in path_config:
                    continue

                path_method_config = path_config[http_method]

                # pprint(path_config)
                module_name, method_name = parse_method_path(path_method_config.get('method'))

                fields = [APIFieldConfig(_) for _ in path_method_config.get('fields', [])]
                field_map = {}
                for field in fields:
                    field_map[field.name] = field

                method_tags = tags + path_method_config.get('tags', [])

                params = {
                    'module_name': module_name,
                    'method_name': method_name,
                    'fields': fields,
                    'tags': method_tags,
                    'field_map': field_map,
                }

                for field, param_field, default_value in self.path_copy_fields:
                    params[param_field] = path_method_config.get(field, default_value)

                method_config = APIMethodConfig(http_methods=[http_method], **params)

                path = self.path_router.add_path(method=http_method, text=path_text, data=method_config)

                # Update param_in (for swagger)
                for field in method_config.fields:
                    for node in path:
                        if node.is_params and node.value == field.name:
                            field.param_in = 'path'
                            field.set_field_type(node.type)
                            break

    @property
    def definitions(self):
        return self.data.get('definitions', {})

    @property
    def tags(self):
        return self.data.get('tags', [])
