# -*- coding: utf-8 -*-
"""
===============================================================================

Copyright (C) 2013/2016 Laurent Labatut / Laurent Champagnac



 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 as published by the Free Software Foundation; either version 2
 of the License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA
 ===============================================================================
"""
import atexit
import logging
import socket
import sys
import time
import ujson
from collections import defaultdict
from contextlib import contextmanager

if sys.version_info > (3, 0):
    # noinspection PyPep8Naming,PyUnresolvedReferences
    import queue as Queue

    custom_range = range
else:
    import Queue

    custom_range = xrange

logger = logging.getLogger(__name__)


class Knock(object):
    """
    Knock singleton
    """

    # Meta
    # __metaclass__ = SingletonMetaClass

    # Counter queue
    QUEUE_COUNTER = Queue.Queue()
    # Dtc queue
    QUEUE_DTC = Queue.Queue()
    # Gauge queue
    QUEUE_GAUGE = Queue.Queue()

    # UDP
    UDP_SOCKET_NAME = "/var/run/knockdaemon.udp.socket"
    UDP_UNITTEST_SOCKET_NAME = "/tmp/knockdaemon.udp.socket"

    # ===============================
    # PUBLIC HELPERS
    # ===============================

    @classmethod
    def increment(cls, item, value):
        """
        Increment item using specified float value
        :param item: item name
        :type item: str,unicode
        :param value: value
        :type value: float
        :return True if success, False otherwise
        :rtype bool
        """
        if not cls._is_clean_item(item):
            return False

        cls.QUEUE_COUNTER.put((item, value))
        return True

    @classmethod
    def gauge(cls, item, value):
        """
        Set gauge item to specified float value
        :param item: item name
        :type item: str,unicode
        :param value: value
        :type value: float
        :return True if success, False otherwise
        :rtype bool
        """
        if not cls._is_clean_item(item):
            return False

        cls.QUEUE_GAUGE.put((item, value))
        return True

    @classmethod
    def start_delay(cls, item):
        """
        Start a DelayToCount. Raise an exception in case of invalid item.
        :param item: str,unicode
        :type item: str,unicode
        :return: tuple time, item
        :rtype: tuple
        """
        if not cls._is_clean_item(item):
            raise TypeError('Item length > 70')
        return time.time(), item

    @classmethod
    def stop_delay(cls, tu):
        """
        Stop a DelayToCount
        :param tu:  tuple time, item
        :type tu: tuple
        :return True if success, False otherwise
        :rtype bool
        """

        try:
            start_time, item = tu

            if not cls._is_clean_item(item):
                return False

        except Exception as e:
            logger.warning('tu (time,item) parameter is wrong! ex=%s', e.message)
            return False

        value = float(time.time() - start_time) * 1000.0
        cls.QUEUE_DTC.put((item, value))

        return True

    # ===============================
    # PUBLIC COMMIT
    # ===============================

    @classmethod
    def commit(cls):
        """
        Send all pending stuff toward knockdaemon UDP listener
        :return bool
        :rtype bool
        """

        # Call it sync
        return cls._internal_commit()

    # ===============================
    # INTERNAL COMMIT
    # ===============================

    @classmethod
    def _internal_commit(cls):
        """
        Send all pending stuff toward knockdaemon UDP listener
        :return bool
        :rtype bool
        """

        # ------------------------
        # Pre-Process
        # ------------------------

        # Counter
        dict_counter = defaultdict(float)
        for item, value in cls._queue_get_all(cls.QUEUE_COUNTER):
            logger.debug('Counter: item=%s, value=%s', item, value)
            dict_counter[item] += value

        # Gauge
        dict_gauge = defaultdict(float)
        for item, value in cls._queue_get_all(cls.QUEUE_GAUGE):
            logger.debug('Gauge: item=%s, value=%s', item, value)
            dict_gauge[item] = value

        # ------------------------
        # Prepare all datas
        # ------------------------

        # Go
        list_to_send = []

        # Delay to count
        for item, value in cls._queue_get_all(cls.QUEUE_DTC):
            logger.debug('Delay to count: item=%s, value=%s', item, value)
            list_to_send.append((item, 'DTC', value))

        # Counter
        for k, v in dict_counter.items():
            list_to_send.append((k, 'C', v))

        # Gauge
        for k, v in dict_gauge.items():
            list_to_send.append((k, 'G', v))

        # ------------------------
        # Send them by chunk toward UDP
        # ------------------------

        if len(list_to_send) > 0:
            logger.info('Commit %s items', len(list_to_send))
            send_count = 0
            send_loop = 0
            for chunk in cls._chunks(list_to_send):
                logger.debug("Sending, chunk=%s", len(chunk))
                if not cls._send(chunk):
                    return False
                # time.sleep(0.001)
                send_count += len(chunk)
                send_loop += 1
            logger.info("Send count=%s, loop=%s", send_count, send_loop)

        # Ok
        return True

    # ===============================
    # QUEUE HELPER
    # ===============================

    @classmethod
    def _queue_get_all(cls, q):
        """
        Return generator of provided queue
        :param q: queue
        :type q: Queue.Queue
        :return: generator
        :rtype generator
        """
        try:
            while True:
                yield q.get_nowait()
        except Queue.Empty:
            pass

    # ===============================
    # UDP SOCKET SEND
    # ===============================

    @classmethod
    def _send(cls, messages):
        """
        Send message to upd
        :param messages: list of tuple (item, type, value)
        :type messages: list
        :return bool
        :rtype bool
        """

        sock = None
        try:
            logger.debug('sending message len=%s', len(messages))
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)  # UDP

            sock.connect(cls.UDP_SOCKET_NAME)

            json_message = ujson.dumps(messages)
            sock.sendall(json_message.encode("utf8"))
            return True

        except Exception as e:
            logger.warning('cant send message ex=%s', e)
            return False
        finally:
            # Close
            cls.safe_close_socket(sock)

    @classmethod
    def safe_close_socket(cls, soc_to_close):
        """
        Safe close a socket
        :param cls: cls
        :param soc_to_close: socket
        :return: Nothing
        """

        if soc_to_close is None:
            return

        try:
            soc_to_close.shutdown(2)
        except Exception as e:
            logger.debug("Socket shutdown ex=%s", e)

        try:
            soc_to_close.close()
        except Exception as e:
            logger.debug("Socket close ex=%s", e)

        try:
            del soc_to_close
        except Exception as e:
            logger.debug("Socket del ex=%s", e)

    # ===============================
    # CLEAN
    # ===============================

    @classmethod
    def _is_clean_item(cls, item):
        """
        Check if item is valid
        :param item: item
        :type item: str
        :return True if ok, False otherwise
        :rtype bool
        """
        if len(item) > 70:
            return False
        return True

    # ===============================
    # CHUNKS
    # ===============================

    @classmethod
    def _chunks(cls, item_list, item_max_count=704):
        """
        Yield successive n-sized chunks from l
        :param item_list: list of (item, type, value)
        :type item_list: list
        :param item_max_count: chunk max size
        :type item_max_count: int
        :return generator, list of item, type, value
        :rtype generator
        """
        for i in custom_range(0, len(item_list), item_max_count):
            yield item_list[i:i + item_max_count]

    @classmethod
    def delay(cls, item):
        """

        Send delay to count probe via a decorator

        :param item: item name
        :type item: str
        :return: func
        :rtype: func
        """

        def decorated(func):
            def wrapper(*args, **kwargs):
                t = cls.start_delay(item)
                response = func(*args, **kwargs)
                cls.stop_delay(t)
                return response

            return wrapper

        return decorated

    @classmethod
    @contextmanager
    def with_delay(cls, item):
        """
        Context manager to sent delay to count probe
        :param item: item name
        :type item: str
        :return:
        :rtype: None
        """
        t = cls.start_delay(item)
        try:

            yield

        finally:
            cls.stop_delay(t)

# Register commit upon exit
atexit.register(Knock.commit)
