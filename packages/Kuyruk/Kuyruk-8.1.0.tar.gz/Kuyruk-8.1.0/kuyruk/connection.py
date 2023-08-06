import logging
import threading

import amqp
import amqp.exceptions

logger = logging.getLogger(__name__)

_CONNECT_TIMEOUT = 5
_READ_TIMEOUT = 5
_WRITE_TIMEOUT = 5


class SingleConnection(object):
    """SingleConnection is a helper for dealing with amqp.Connection objects
    from multiple threads."""

    def __init__(self,
                 host='localhost',
                 port=5672,
                 user='guest',
                 password='guest',
                 vhost='/'):
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._vhost = vhost

        self._connection = None
        self._lock = threading.RLock()
        self._heartbeat_started = False
        self._closed = threading.Event()

    def __enter__(self):
        self._lock.acquire()
        return self.get()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._lock.release()
        return False

    @property
    def lock(self):
        """Returns the threading.RLock object for this connection.
        Concurrent access to the connected must be protected this lock."""
        return self._lock

    def get(self):
        """Returns the underlying connection if it is already connected.
        Creates a new connection if necessary."""
        with self._lock:
            if self._connection is None:
                return self._connect()

            if not self._is_alive():
                self._remove()
                return self._connect()

            if not self._heartbeat_started:
                heartbeat = threading.Thread(target=self._heartbeat_sender)
                heartbeat.daemon = True
                heartbeat.start()
                self._heartbeat_started = True

            return self._connection

    def close(self):
        """Close the underlying connection."""
        with self._lock:
            if self._connection is not None:
                self._connection.close()

    def _connect(self):
        """Open new connection and save the object."""
        conn = self._new_connection()
        self._connection = conn
        return conn

    def _is_alive(self):
        """Check aliveness by sending a heartbeat frame."""
        try:
            self._connection.send_heartbeat()
        except IOError:
            return False
        else:
            return True

    def _new_connection(self):
        """Returns a new connection."""
        conn = amqp.Connection(
            host="%s:%d" % (self._host, self._port),
            userid=self._user,
            password=self._password,
            virtual_host=self._vhost,
            connect_timeout=_CONNECT_TIMEOUT,
            read_timeout=_READ_TIMEOUT,
            write_timeout=_WRITE_TIMEOUT)
        logger.debug("connecting to amqp")
        conn.connect()
        return conn

    def _remove(self):
        """Close the connection and dispose connection object."""
        logger.debug("closing connection")
        try:
            self._connection.close()
        except Exception:
            pass
        self._connection = None

    def _heartbeat_sender(self):
        """Target function for heartbeat thread."""
        while not self._closed.wait(1):
            with self._lock:
                if self._closed.is_set():
                    return

                if self._connection is None:
                    continue

                logger.debug("sending heartbeat")
                try:
                    self._connection.heartbeat_tick()
                except Exception as e:
                    logger.warning("Cannot send heartbeat: %s", e)
                    # There must be a connection error.
                    # Let's make sure that the connection is closed
                    # so next publish call can create a new connection.
                    self._remove()
