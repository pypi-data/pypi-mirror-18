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

import knockprobe
from knockprobe.Singleton import SingletonMetaClass

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
    __metaclass__ = SingletonMetaClass

    # Counter queue
    QUEUE_COUNTER = Queue.Queue()
    # Dtc queue
    QUEUE_DTC = Queue.Queue()
    # Gauge queue
    QUEUE_GAUGE = Queue.Queue()

    # UDP
    UDP_IP = "127.0.0.1"
    UDP_PORT = 63184

    def __init__(self):
        """
        Init
        """
        pass

    # ===============================
    # PUBLIC HELPERS
    # ===============================

    @classmethod
    def increment(cls, item, value):
        """
        Increment item using specified float value
        :param item: item name
        :type item: str
        :param value: value
        :type value: float
        :return True if success, False otherwise
        :rtype bool
        """
        if not Knock._is_clean_item(item):
            return False

        Knock.QUEUE_COUNTER.put((item, value))
        return True

    @classmethod
    def gauge(cls, item, value):
        """
        Set gauge item to specified float value
        :param item: item name
        :type item: str
        :param value: value
        :type value: float
        :return True if success, False otherwise
        :rtype bool
        """
        if not Knock._is_clean_item(item):
            return False

        Knock.QUEUE_GAUGE.put((item, value))
        return True

    @classmethod
    def start_delay(cls, item):
        """
        Start a DelayToCount. Raise an exception in case of invalid item.
        :param item: str
        :type item: str
        :return: tuple time, item
        :rtype: tuple
        """
        if not Knock._is_clean_item(item):
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

            if not Knock._is_clean_item(item):
                return False

        except Exception as e:
            logger.warning('tu (time,item) parameter is wrong! ex=%s', e.message)
            return False

        value = time.time() - start_time
        Knock.QUEUE_DTC.put((item, value))

        return True

    # ===============================
    # PUBLIC COMMIT
    # ===============================

    @classmethod
    def commit(cls):
        """
        Send all pending stuff toward knockdaemon UDP listener
        If gevent is available, fire async using a gevent.spawn
        Otherwise, fire sync.
        """
        if knockprobe.gevent_imported():
            # noinspection PyPackageRequirements
            import gevent
            # Spawn
            gevent.spawn(Knock._internal_commit)
            # Context switch
            gevent.sleep(0.0)
        else:
            # Call it sync
            Knock._internal_commit()

    # ===============================
    # INTERNAL COMMIT
    # ===============================

    @classmethod
    def _internal_commit(cls):
        """
        Send all pending stuff toward knockdaemon UDP listener
        """

        # ------------------------
        # Pre-Process
        # ------------------------

        # Counter
        dict_counter = defaultdict(float)
        for item, value in Knock._queue_get_all(Knock.QUEUE_COUNTER):
            logger.debug('Counter: item=%s, value=%s', item, value)
            dict_counter[item] += value

        # Gauge
        dict_gauge = defaultdict(float)
        for item, value in Knock._queue_get_all(Knock.QUEUE_GAUGE):
            logger.debug('Gauge: item=%s, value=%s', item, value)
            dict_gauge[item] = value

        # ------------------------
        # Prepare all datas
        # ------------------------

        # Go
        list_to_send = []

        # Delay to count
        for item, value in Knock._queue_get_all(Knock.QUEUE_DTC):
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
            for chunk in Knock._chunks(list_to_send):
                Knock._send(chunk)

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
        """
        udp_ip = Knock.UDP_IP
        upd_port = Knock.UDP_PORT
        try:
            json_message = ujson.dumps(messages)
            logger.debug('sending message len=%s', len(messages))
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
            sock.connect((udp_ip, upd_port))
            sock.sendall(json_message.encode())
            sock.close()
        except Exception as e:
            logger.warning('cant send message ex=%s', e.message)

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
                t = Knock.start_delay(item)
                response = func(*args, **kwargs)
                Knock.stop_delay(t)
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
        t = Knock.start_delay(item)
        try:

            yield

        finally:
            Knock.stop_delay(t)

# Register commit upon exit
atexit.register(Knock.commit)
