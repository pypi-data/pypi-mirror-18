# Copyright (c) 2016 Cyso < development [at] cyso . com >
#
# This file is part of omniconf, a.k.a. python-omniconf .
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3.0 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library. If not, see
# <http://www.gnu.org/licenses/>.


class UnknownSettingError(Exception):
    """
    Trying to configure a value for an unknown Setting.
    """
    pass


class UnconfiguredSettingError(Exception):
    """
    Trying to retrieve a value which has not been configured yet.
    """
    pass


class InvalidBackendConfiguration(Exception):
    """
    Trying to configure a backend with invalid configuration.
    """
    pass
