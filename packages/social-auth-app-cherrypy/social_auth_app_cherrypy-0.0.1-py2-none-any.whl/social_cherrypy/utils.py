import warnings
from functools import wraps

import cherrypy

from social_core.utils import setting_name, module_member, get_strategy
from social_core.backends.utils import get_backend, user_backends_data


DEFAULTS = {
    'STRATEGY': 'social_cherrypy.strategy.CherryPyStrategy',
    'STORAGE': 'social_cherrypy.models.CherryPyStorage'
}


def get_helper(name):
    return cherrypy.config.get(setting_name(name), DEFAULTS.get(name, None))


def load_backend(strategy, name, redirect_uri):
    backends = get_helper('AUTHENTICATION_BACKENDS')
    Backend = get_backend(backends, name)
    return Backend(strategy=strategy, redirect_uri=redirect_uri)


def psa(redirect_uri=None):
    def decorator(func):
        @wraps(func)
        def wrapper(self, backend=None, *args, **kwargs):
            uri = redirect_uri
            if uri and backend and '%(backend)s' in uri:
                uri = uri % {'backend': backend}
                if uri[-1] != '/' and \
                   cherrypy.config.get(setting_name('TRAILING_SLASH'), False):
                    uri = uri + '/'
            self.strategy = get_strategy(get_helper('STRATEGY'),
                                         get_helper('STORAGE'))
            self.backend = load_backend(self.strategy, backend, uri)
            return func(self, backend, *args, **kwargs)
        return wrapper
    return decorator


def backends(user):
    """Load Social Auth current user data to context under the key 'backends'.
    Will return the output of social_core.backends.utils.user_backends_data."""
    return user_backends_data(user, get_helper('AUTHENTICATION_BACKENDS'),
                              module_member(get_helper('STORAGE')))


def strategy(*args, **kwargs):
    warnings.warn('@strategy decorator is deprecated, use @psa instead')
    return psa(*args, **kwargs)
