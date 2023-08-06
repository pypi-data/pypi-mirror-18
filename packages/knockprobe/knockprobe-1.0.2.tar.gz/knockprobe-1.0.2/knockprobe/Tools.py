"""
-*- coding: utf-8 -*-
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
from sys import modules


def gevent_imported():
    """
    Is gevent imported
    :return bool
    :rtype bool
    """
    if hasattr(gevent_imported, '__GEVENT_IMPORTED'):
        return gevent_imported.__GEVENT_IMPORTED
    else:
        if 'gevent' in modules:
            # noinspection PyPep8Naming
            GEVENT_IMPORTED = True
        else:
            # noinspection PyPep8Naming
            GEVENT_IMPORTED = False

        setattr(gevent_imported, '__GEVENT_IMPORTED', GEVENT_IMPORTED)

        return GEVENT_IMPORTED
