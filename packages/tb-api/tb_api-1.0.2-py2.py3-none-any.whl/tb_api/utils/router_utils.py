import re

from tb_api.model.router import RouterResult

param_pattern = re.compile('/?([^/]+)(.*)')


def search_url(node, url, params={}):
    if node.is_text:
        if not url.startswith(node.value):
            # not match
            return RouterResult.not_match(params)

        remain_url = url[len(node.value):]
        # print 'text remain url', remain_url, node.data, remain_url == ""
        if remain_url == "":
            # match
            return RouterResult(node.data, params)

        return _search_child(node, remain_url, params)
    else:
        # param
        m = param_pattern.search(url)
        if not m:
            # Not match
            return RouterResult.not_match(params)

        param_value = m.group(1)
        remain_url = m.group(2)
        # print 'remain_url', remain_url
        if remain_url == "":
            # Done
            return _build_search_result(node, param_value, params)
        else:
            result = _search_child(node, remain_url, params)
            if not result.match:
                # Not match
                return result
            else:
                # Match
                return _build_search_result(node, param_value, params, data=result.data, other_params=result.params)


def _build_search_result(node, value, params, data=None, other_params={}):
    ret_params = params.copy()
    ret_params.update(other_params)
    ret_params[node.value] = node.parse_value(value)
    if data is None:
        data = node.data

    return RouterResult(data, ret_params)


def _search_child(node, url, params):
    for child_node in node:
        result = search_url(child_node, url, params)
        if result.match:
            # Child match
            return result

    # Not match
    return RouterResult.not_match(params)
