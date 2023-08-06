# Copyright (c) AppDynamics, Inc., and its affiliates
# 2015
# All Rights Reserved

"""Interceptors for dealing with DB-API 2.0 compatible libraries.

"""

from __future__ import unicode_literals
import abc

from appdynamics.lang import str
from appdynamics.agent.models.exitcalls import EXIT_DB, EXIT_SUBTYPE_DB
from .. import HOST_PROPERTY_MAX_LEN, DB_NAME_PROPERTY_MAX_LEN, VENDOR_PROPERTY_MAX_LEN
from ..base import ExitCallInterceptor


class DbAPICursorInterceptor(ExitCallInterceptor):
    def _execute(self, execute, cursor, operation, *args, **kwargs):
        exit_call = None
        with self.log_exceptions():
            bt = self.bt
            if bt:
                backend = self.get_connection(cursor)._appd_backend
                if backend and not hasattr(cursor, '_appd_exit_call'):
                    exit_call = self.start_exit_call(bt, backend, operation=operation)
                    cursor._appd_exit_call = exit_call

        result = execute(cursor, operation, appd_exit_call=exit_call,
                         *args, **kwargs)

        # Normally it's fine to just try to end the exit call even if we
        # aren't sure it actually started.  However for cases where we have
        # several `execute` calls nested inside an `executemany` call, we do
        # not want to end the exit call until the outer call is over.
        if exit_call:
            self.end_exit_call(exit_call=exit_call)
            try:
                delattr(cursor, '_appd_exit_call')
            except AttributeError:
                pass
        return result

    @abc.abstractmethod
    def get_connection(self, cursor):
        """Return the `Connection` object used to create this `Cursor`.

        """
        pass


class DbAPIConnectionInterceptor(ExitCallInterceptor):
    backend_naming_format_string = '{HOST}:{PORT} - {DATABASE} - {VENDOR} - {VERSION}'

    def __init__(self, agent, cls, cursor_interceptor, vendor):
        super(DbAPIConnectionInterceptor, self).__init__(agent, cls)
        self.vendor = vendor[:VENDOR_PROPERTY_MAX_LEN]
        self.cursor_interceptor = cursor_interceptor

    def attach(self, connect_func):
        super(DbAPIConnectionInterceptor, self).attach(connect_func, patched_method_name='_connect')
        super(DbAPIConnectionInterceptor, self).attach('cursor')

    def get_backend(self, connection, *args, **kwargs):
        host, port, dbname = self.get_backend_properties(connection, *args, **kwargs)

        host = host[:HOST_PROPERTY_MAX_LEN]
        dbname = dbname[:DB_NAME_PROPERTY_MAX_LEN]

        backend_properties = {
            'VENDOR': self.vendor,
            'HOST': host,
            'PORT': str(port),
            'DATABASE': dbname,
            'VERSION': 'unknown',
        }

        return self.agent.backend_registry.get_backend(EXIT_DB, EXIT_SUBTYPE_DB, backend_properties,
                                                       self.backend_naming_format_string)

    def _connect(self, connect, connection, *args, **kwargs):
        with self.log_exceptions():
            exit_call = None
            if self.agent.enabled:
                # Store the backend on the connection object, even if there is
                # no active BT.
                backend = self.get_backend(connection, *args, **kwargs)
                connection._appd_backend = backend

                bt = self.bt
                if bt and backend:
                    exit_call = self.start_exit_call(bt, backend, operation='connect')
        connect(connection, appd_exit_call=exit_call, *args, **kwargs)
        self.end_exit_call(exit_call)

    def _cursor(self, cursor, connection, *args, **kwargs):
        cursor_instance = cursor(connection, appd_exit_call=None, *args, **kwargs)
        with self.log_exceptions():
            self.cursor_interceptor(self.agent, type(cursor_instance)).attach(['execute', 'executemany'],
                                                                              patched_method_name='_execute')
        return cursor_instance

    @abc.abstractmethod
    def get_backend_properties(self, connection, *args, **kwargs):
        """Return a tuple of (host, port, database) for this `Connection`.

        The parameters passed to this function are the same as those passed to
        the intercepted `connect` function.

        WARNING: `connection` may not have been initialized when this
        function is called; be careful.

        """
        pass
