import re

import six

from tb_api.model.path import PathTextNode, PathParamNode, Path
from tb_api.model.router import RouterResult
from tb_api.utils.router_utils import search_url


class PathRouter(object):
    path_pattern = re.compile('([^{}]+|{(\w+)(:(\w+))?})')
    support_methods = ['get', 'post', 'put', 'patch', 'delete']

    def __init__(self):
        self._tree = {}
        for method in self.support_methods:
            self._tree[method] = PathTree()

    def __getitem__(self, key):
        return self._tree[key]

    @property
    def trees(self):
        for method in self.support_methods:
            yield self[method]

    @property
    def method_trees(self):
        for method in self.support_methods:
            yield method, self[method]

    # @property
    # def get(self):
    #     return self._tree['get']
    #
    # @property
    # def post(self):
    #     return self._tree['post']
    #
    # @property
    # def put(self):
    #     return self._tree['put']
    #
    # @property
    # def patch(self):
    #     return self._tree['patch']
    #
    # @property
    # def delete(self):
    #     return self._tree['delete']

    def add_path(self, method, text, data):
        if not text:
            text = '/'

        m = self.path_pattern.findall(text)
        # print m
        if not m:
            raise InvalidPathError(text)

        path = Path()
        for text, param, _, param_type in m:
            # print 'path', text, param, param_type
            if not param:
                node = PathTextNode(text)
            else:
                node = PathParamNode(param, param_type=param_type)

            path.add(node)

        self._add_path(method, path, data)

        return path

    def _add_path(self, method, path, data):
        # print path[0]
        tree = self[method]
        tree.add(path, data)

    def search(self, method, url):
        tree = self[method]

        return tree.search(url)


class InvalidPathError(Exception):
    pass


def path_to_branch(path, data):
    root = None
    current_node = None
    # print 'patha', path[0], '-', path[1]
    for node in path:
        # print 'node', node
        if root is None:
            root = node
            current_node = node
        else:
            # print 'add_child', current_node, node
            current_node.add_child(node)
            current_node = node

    current_node.data = data

    return root


def merge_node(root_node, path_nodes, data):
    if not path_nodes:
        return

    first_path_node = path_nodes[0]

    for child_node in root_node:
        if child_node == first_path_node:
            merge_node(child_node, path_nodes[1:], data)
            return

    root_node.add_child(path_to_branch(path_nodes, data))


class PathTree(object):
    def __init__(self):
        self._tree = []
        self.paths = []

    def add(self, path, data):
        self.paths.append((path, data))

        for root in self._tree:
            if root == path[0]:
                # Merge to this node
                # print 'merge'
                merge_node(root, path[1:], data)
                # print root

                return

        # Create new node
        root = path_to_branch(path, data)

        self._tree.append(root)

    def search(self, url):
        # TODO Improve performance
        for root in self._tree:
            result = search_url(root, url)
            if result.match:
                return result

        return RouterResult.not_match()
