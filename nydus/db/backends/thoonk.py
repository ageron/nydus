"""
nydus.db.backends.thoonk
~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2011 DISQUS.
:license: Apache License 2.0, see LICENSE for more details.
"""

from __future__ import absolute_import

from thoonk import Pubsub

from redis import exceptions as client_exceptions

from nydus.db.backends import BaseConnection

# from nydus.db.backends import BasePipeline


# class ThoonkPipeline(BasePipeline):
#     def __init__(self, connection):
#         self.pending = []
#         self.connection = connection
#         self.pipe = connection.pipeline()

#     def add(self, command):
#         self.pending.append(command)
#         getattr(self.pipe, command._attr)(*command._args, **command._kwargs)

#     def execute(self):
#         return self.pipe.execute()


class Thoonk(BaseConnection):
    # Exceptions that can be retried by this backend
    retryable_exceptions = client_exceptions
    supports_pipelines = False

    def __init__(self, host='localhost', port=6379, db=0, timeout=None, listen=False, **options):
        self.host = host
        self.port = port
        self.db = db
        self.timeout = timeout
        self.pubsub = None
        self.listen = listen
        super(Thoonk, self).__init__(**options)

    @property
    def identifier(self):
        mapping = vars(self)
        mapping['klass'] = self.__class__.__name__
        return "redis://%(host)s:%(port)s/%(db)s" % mapping

    def connect(self):
        return Pubsub(host=self.host, port=self.port, db=self.db, listen=self.listen)

    def disconnect(self):
        self.pubsub.close()

    # def get_pipeline(self, *args, **kwargs):
    #     return ThoonkPipeline(self)

    def __getattr__(self, attr):
        """
        Treat the pubsub as the first class object here,
        fail over to the redis connection
        """
        return getattr(self.connection, attr)
