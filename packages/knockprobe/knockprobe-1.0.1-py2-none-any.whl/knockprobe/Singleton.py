"""
-*- coding: utf-8 -*-
===============================================================================

Copyright (C) 2013/2016 Laurent Labatut



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
import logging

import knockprobe

logger = logging.getLogger(__name__)

if knockprobe.__GEVENT_IMPORTED:
    logger.info('Import Lock from Gevent')
    # noinspection PyPackageRequirements
    from gevent.threading import Lock
else:
    logger.info('Import Lock from threading python')
    from threading import Lock



class SingletonMetaClass(type):
    """
    Usage :
    class mysingleton(Object):

        __metaclass__ = Singleton

    """
    __singleton_lock = Lock()
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Override
        :param args: args
        :param kwargs: kwargs
        :return object
        """
        if cls not in cls._instances:
            with cls.__singleton_lock:
                if cls not in cls._instances:
                    # noinspection PyArgumentList
                    cls._instances[cls] = super(SingletonMetaClass, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
