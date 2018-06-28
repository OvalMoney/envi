"""Top-level package for envi."""
from .envi import (
    get, mk_shortcut, get_int, get_bool, get_float, get_str, IS_OK  # noqa
)

__all__ = [
    'get', 'mk_shortcut', 'get_float', 'get_int', 'get_bool', 'get_str', 'IS_OK'
]

__author__ = """Simone Basso"""
__email__ = 'simone.basso1990@gmail.com'
__version__ = '0.1.0'
