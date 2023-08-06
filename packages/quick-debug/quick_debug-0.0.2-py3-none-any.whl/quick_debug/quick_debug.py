"""File containing simple debug's code."""
from __future__ import print_function
import sys
import logging
logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger()


def quick_debug(func):
    """Decorate functions to have control over whether to debug or not.

    NOTE: bool `debug` kwarg is expected.

    NOTE: The functions that are decorated by this decorater only need to use,
        logger.DEBUG to have control over whether DEBUG logs are printed on
        screen or not.

    NOTE: The functions that are decorated by this decorater cannot have a kwarg
        named `bool`.

    NOTE: Print function continues to work as is in the functions that are decorated
        by this decorater.
    """
    def func_wrapper(*args, **kwargs):
        # set logging level as DEBUG for this function sepecifically.
        debug = kwargs.get('debug', False)
        if debug:
            logging.disable(logging.NOTSET)
            logger.setLevel(logging.DEBUG)
            logger.debug("============================================= {}".format(func.__name__))

        # remove the debug argument before passing onto the function.
        kwargs.pop('debug', None)

        # pass args and kwargs as is to the function
        ret_val = func(*args, **kwargs)

        # reset logging level to the glo
        logging.disable(logging.DEBUG)

        # return ret_val as is
        return ret_val

    return func_wrapper
