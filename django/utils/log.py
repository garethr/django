from django.utils.importlib import import_module
from django.core.exceptions import ImproperlyConfigured
import logging

class NullHandler(logging.Handler): 
    def emit(self, record): 
        pass

logger = logging.getLogger('django')
logger.setLevel(logging.INFO)
if len(logger.handlers) == 0:
    logger.addHandler(NullHandler())
logger.propagate = False

def configure_from_dict(configuration):
    "Configure loggers using a settings.LOGGING style dictionary"
    for logger_label, config in configuration.items():
        logger = logging.getLogger(logger_label)
        level = config.pop('level', None)
        if level is not None:
            if level.isdigit():
                level_int = int(level)
            else:
                level_int = getattr(logging, level.upper(), None)
                if level_int is None:
                    raise ImproperlyConfigured, \
                        '"%s" is not a valid logging level' % level
            logger.setLevel(level_int)
        handler = config.pop('handler', None)
        if handler is not None:
            klass = handler_from_string(handler)
            logger.addHandler(klass(**config))

def handler_from_string(string):
    # Could refactor with django.core.handlers.base.BaseHandler.load_middleware
    try:
        dot = string.rindex('.')
    except ValueError:
        raise ImproperlyConfigured, '%s isn\'t a handler module' % string
    module, classname = string[:dot], string[dot+1:]
    try:
        mod = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured, 'Error importing handler %s: "%s"' % (module, e)
    try:
        klass = getattr(mod, classname)
    except AttributeError:
        raise ImproperlyConfigured, 'Module "%s" does not define a "%s" class' % (module, classname)
    return klass
