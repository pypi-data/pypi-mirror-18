import importlib
import six

import bottle

__version__ = '0.1.0'

__all__ = [
    'ApiError',
    'BottleStonePlugin',
]


class ApiError(Exception):
    """
    The BottleStonePlugin catches ApiError objects and converts them to error
    responses.
    """

    def __init__(self, error):
        """
        Args:
             error (object): An instance of the error data type for the route.
        """
        self.error = error

    def __repr__(self):
        return 'ApiError(%r)' % self.error


class BottleStonePlugin(object):
    """
    Install::

        > import bottle
        > bottle.install(BottleStonePlugin('yomua.datatypes'))

    Conforms to the Bottle Plugin v2 protocol.
    """

    api = 2

    name = 'bottle_stone_plugin'

    def __init__(self, package_path, error_http_status_code=418):
        """
        Args:
            package_path: The package containing code generated using the Stone
                "python_types" generator.
            error_http_status_code: The HTTP status code to return for error
                responses.
        """
        assert isinstance(package_path, six.text_type), \
            'Expected text, got %r' % package_path
        self._package_path = package_path

        # Basic check that the package_path exists
        assert importlib.import_module(package_path), \
            'Could not import %s' % package_path

        # Import generated modules that we expect to be there
        self._stone_validators = importlib.import_module(
            package_path + '.stone_validators')
        self._stone_serializers = importlib.import_module(
            package_path + '.stone_serializers')
        self._json_encode = self._stone_serializers.json_compat_obj_encode
        self._json_decode = self._stone_serializers.json_compat_obj_decode

        self._error_http_status_code = error_http_status_code

    def apply(self, callback, route):
        if route.name is None:
            return callback

        namespace, route_name = route.name.split('.', 1)

        # Based on the Stone python_types generator, we expect the namespace
        # of a given route to map to a module within package_path.
        namespace_module = importlib.import_module(
            self._package_path + '.' + namespace)

        # Extract the Stone description of the route.
        stone_route = getattr(namespace_module, route_name)

        # Bottle will cache this wrapped_callback.
        def wrapped_callback():
            try:
                arg = self._json_decode(
                    stone_route.arg_type, bottle.request.json)
            except self._stone_validators.ValidationError as e:
                # We treat validation errors as 400 Bad Request.
                bottle.response.status = 400
                msg = 'Error in call to {}: request body: {}'.format(
                    bottle.request.path, str(e))
                return dict(error=msg)

            try:
                res_obj = callback(arg)
            except ApiError as e:
                bottle.response.status = self._error_http_status_code
                return self._json_encode(stone_route.error_type, e.error)
            else:
                return self._json_encode(stone_route.result_type, res_obj)

        return wrapped_callback
