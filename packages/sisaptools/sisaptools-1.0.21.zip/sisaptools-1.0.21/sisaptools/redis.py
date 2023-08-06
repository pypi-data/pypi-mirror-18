# -*- coding: utf8 -*-

"""
Eines per a la connexió a Redis.
"""

from __future__ import absolute_import
import redis

from .constants import APP_CHARSET, IS_PYTHON_3


ALIASES = {'sisap': ('redis', 6379)}


class Redis(redis.StrictRedis):
    """
    Modificació de StrictRedis per poder instanciar de
    forma transparent segons la versió de l'intèrpret.
    """

    def __init__(self, alias):
        host, port = ALIASES[alias]
        redis.StrictRedis.__init__(
            self,
            host=host,
            port=port,
            charset=APP_CHARSET,
            decode_responses=IS_PYTHON_3
        )
