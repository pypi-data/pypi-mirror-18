from tb_ioc import IOC

from tb_api.exception import UnauthorizedError, InvalidMethodError, InvalidServiceMethodError
from tb_api.loader.core import Loader
from tb_api.model.config import APIConfig


class LoaderIOC(Loader):
    def __init__(self, config_files, module_suffix=''):
        self.module_suffix = module_suffix
        self.ioc = IOC()
        for config_file in config_files:
            self.ioc.load_file(config_file)

        self.extra_app_handlers = []
        cors_params = self.ioc.get_parameter('API_CORS')
        if cors_params:
            self.ioc.load({
                'services': {
                    'API_FlaskCORS': {
                        'class': 'tb_api.app_handler.cors.FlaskCORS',
                        'arguments': [cors_params]
                    }
                }
            })

            self.extra_app_handlers.append('API_FlaskCORS')

        if not module_suffix:
            self.module_suffix = self.ioc.get_parameter('API_ModuleSuffix')

        self.config = APIConfig(self.ioc.get_parameter('API_Config', {}))
        self._cache_methods = {}

    def get_method(self, http_method, url):
        router_result = self.config.get_config(http_method, url)

        if not router_result.match:
            raise UnauthorizedError(http_method, url)

        method_config = router_result.data
        module_name = method_config.module_name
        method_name = method_config.method_name

        key = '%s-%s' % (module_name, method_name)
        if key not in self._cache_methods:
            if self.module_suffix:
                service_name = '%s%s' % (module_name, self.module_suffix)
            else:
                service_name = module_name

            obj = self.ioc.get(service_name)
            try:
                method = getattr(obj, method_name)
            except AttributeError:
                raise InvalidServiceMethodError(service_name, method_name)

            # Decor method. useful for authentication check or variable converter
            for decor_name in method_config.require:
                decor = self.ioc.get(decor_name)
                method = decor(method)

            self._cache_methods[key] = method, method_config

        return self._cache_methods[key], router_result.params

    def json_dump_cls(self):
        return self.ioc.get_parameter('API_Dumper')

    def secret_key(self):
        return self.ioc.get_parameter('API_SecretKey')

    def get_app_handlers(self):
        handler_names = self.ioc.get_parameter('API_AppHandler', [])
        ret = []
        for name in handler_names:
            ret.append(self.ioc.get(name))

        for name in self.extra_app_handlers:
            ret.append(self.ioc.get(name))

        return ret

    def get_ignore_fields(self):
        return self.ioc.get_parameter('API_IgnoreFields', [])

    @property
    def api_version(self):
        return self.ioc.get_parameter('API_Version')
