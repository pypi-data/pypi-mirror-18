from six.moves.urllib.parse import urlparse

from flask import request


def flask_build_swagger(config, api_url_prefix):
    o = urlparse(request.url_root)

    return build_swagger(config, o.netloc, api_url_prefix)


def build_swagger(config, host, api_url_prefix="/api"):
    paths = _build_paths(config)

    return {
        "swagger": "2.0",
        "info": {
            "description": "",
            "version": "1.0.0",
            "title": "API",
            "termsOfService": "",
            "contact": {
                "email": ""
            },
            "license": {
                "name": "",
                "url": ""
            }
        },
        "host": host,
        "basePath": api_url_prefix,
        "schemes": [
            "http"
        ],
        "paths": paths,
        "definitions": config.definitions,
        "tags": config.tags,
    }


def _build_method_paths(method_config):
    ret = {}

    for method in method_config.http_methods:
        parameters = []
        for field in method_config.fields:
            parameter = {
                'name': field.name,
                'in': field.param_in,
                'description': field.description,
                'required': field.required,
            }

            if field.defaultValue:
                parameter['default'] = field.defaultValue

            if field.type == 'boolean':
                parameter['type'] = 'string'
                parameter["enum"] = ["true", "false"]
            elif field.type:
                parameter['type'] = field.type
            else:
                parameter['type'] = 'string'

            if field.schema:
                parameter['schema'] = {
                    "$ref": "#/definitions/%s" % field.schema
                }

            parameters.append(parameter)

        ret[method] = {
            "summary": method_config.summary,
            "parameters": parameters,
            # 'produces': [
            #     "text/html",
            #     "application/json",
            # ],
            'tags': method_config.tags,
            'responses': {
                200: {
                    'description': "Successful operation",
                },
                404: {
                    'description': "Invalid request"
                },
                500: {
                    'description': 'Internal Server error'
                },
            },
        }

        copy_fields = ['description', 'deprecated']
        for field in copy_fields:
            value = getattr(method_config, field)
            if value:
                ret[method][field] = value

    return ret


def _path_to_swagger_url(path):
    ret = []
    for node in path:
        if node.is_text:
            ret.append(node.value)
        else:
            ret.append('{%s}' % node.value)

    return ''.join(ret)


def _build_paths(config):
    ret = {}

    path_router = config.path_router
    for method, path_tree in path_router.method_trees:
        # print method, path_tree
        # path_tree = path_router[method]
        for path, data in path_tree.paths:
            url = _path_to_swagger_url(path)
            # print url, data
            if url not in ret:
                ret[url] = {}

            ret[url].update(_build_method_paths(data))

            # for node in path:
            #     print 'node', node

    # for module_path in config.path_map:
    #     module_config = config.path_map[module_path]
    #     for method_path in module_config:
    #         method_config = module_config[method_path]
    #         ret['/%s/%s' % (module_path, method_path)] = _build_method_paths(method_config)

    return ret
