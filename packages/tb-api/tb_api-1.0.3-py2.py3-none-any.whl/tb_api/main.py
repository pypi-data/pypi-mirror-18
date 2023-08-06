# encoding=utf-8
import logging
from copy import deepcopy
from os.path import exists, join

from flask import Flask
from flask import Response
from flask import request

from tb_api.crossdomain import crossdomain
from tb_api.exception import APIError, format_html
from tb_api.router import PathRouter
from tb_api.utils.json_utils import JsonDumper
from tb_api.utils.loader_utils import get_api_url_prefix
from tb_api.utils.param_utils import parse_request_param
from tb_api.utils.response_utils import build_error_response, error_response, build_response
from tb_api.utils.swagger_utils import flask_build_swagger

format_field = '_format'
supported_static_files = set(['favicon.ico'])


def load_app(loader, static_folder='static', project_dir=None, debug=False):
    app = Flask(__name__, static_folder=static_folder)
    json_dumper = JsonDumper(cls=loader.json_dump_cls())
    ignore_fields = set([format_field, '_'] + loader.get_ignore_fields())

    # Load the secret key if any
    secret_key = loader.secret_key()
    if secret_key:
        app.secret_key = secret_key

    # Execute handlers
    for handler in loader.get_app_handlers():
        handler(app)

    static_index_file = join(project_dir, 'index.html')

    api_url_prefix = get_api_url_prefix(loader)

    @app.route("/")
    def index():
        if static_index_file:
            if exists(static_index_file):
                return open(static_index_file).read()
            else:
                return "File %s does not exists" % static_index_file

        return "Hello World!"

    def _handle_api(url, http_method):
        try:
            # module_name = module_name.replace('-', '_')
            # method_name = method_name.replace('-', '_')
            (method, method_config), path_params = loader.get_method(http_method, url)
            # print(method)

            # Copy parameters in path to avoid
            params = deepcopy(path_params)

            # Get parameters from url
            for k in request.args.keys():
                if k in ignore_fields:
                    continue
                # print(k)
                params[k] = parse_request_param(method_config, field=k, value=request.args.get(k))

            # Get parameters from body
            request_json = None
            try:
                request_json = request.get_json()
            except:
                # Invalid json in body
                pass

            if request_json:
                for field in request_json:
                    params[field] = parse_request_param(method_config, field=field, value=request_json[field])

            # Load file
            if request.files:
                for field in request.files:
                    params[field] = request.files[field]

            data = method(**params)
            if isinstance(data, Response):
                return data

            try:
                # print(data)
                content = json_dumper.dumps(data)
            except Exception as e:
                print ('Error when dump json: {0}. Data: {1}'.format(str(e), data))
                raise
            return Response(content,
                            mimetype="application/json")
        except APIError as e:
            error_message = str(e)
            mimetype = None

            # return request.args.get(format_field)
            if request.args.get(format_field) == 'html':
                content = format_html(error_message)
                mimetype = 'text/html'
            else:
                content = json_dumper.dumps({
                    'ok': False,
                    'message': error_message
                })
                mimetype = 'application/json'

            return Response(content, status=404,
                            mimetype=mimetype)
        except Exception as e:
            logging.exception(e)

            if hasattr(e, 'to_json'):
                return build_error_response(e.to_json())
            else:
                if request.args.get(format_field) == 'html':
                    # TODO Handle this case
                    raise
                else:
                    debug_url = request.url
                    if '?' in debug_url:
                        debug_url += '&'
                    else:
                        debug_url += '?'

                    return build_error_response({
                        'ok': False,
                        'message': str(e),
                        'hint': 'Access {0}_format=html for more info'.format(debug_url)
                    })

    @app.route(api_url_prefix + "/<path:path>", methods=PathRouter.support_methods)
    def api_call(path):
        return _handle_api('/%s' % path, http_method=request.method.lower())

    # @app.route("/api/<module_name>/<method_name>")
    # def api_call_full(module_name, method_name):
    #     # print(request.args)
    #
    #     return _handle_api(module_name, method_name)

    @app.route(api_url_prefix + "/swagger.json")
    @crossdomain(origin='*')
    def swagger():
        data = flask_build_swagger(loader.config, api_url_prefix=api_url_prefix)
        return build_response(json_dumper, data)

    @app.route("/<path>")
    def static_file(path):
        if path in supported_static_files:
            real_path = join(project_dir, path)
            if exists(real_path):
                return open(real_path, 'rb').read()

        return error_response('Unknown file %s' % path)

    return app
