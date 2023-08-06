# encoding=utf-8

from flask_cors import CORS


class FlaskCORS(object):
    def __init__(self, resources):
        """

        :param resources: Resource config of flask-cors. Example: `{r"/api/*": {"origins": "*"}}`
        :type resources: dict
        """
        self.resources = resources

    def __call__(self, app):
        CORS(app, resources=self.resources)
