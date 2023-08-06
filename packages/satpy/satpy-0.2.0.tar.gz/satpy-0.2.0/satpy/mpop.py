# -*- coding: utf-8 -*-
# Copyright (c) 2014
#
# Author(s):
#
#   Panu Lahtinen <pnuu+git@iki.fi>
#
# This file is part of satpy.
#
# satpy is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# satpy is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# satpy.  If not, see <http://www.gnu.org/licenses/>.

'''MPOP compatibility layer.
'''

import satpy.scene


class GeostationaryFactory(object):

    """Factory for geostationary satellite scenes.
    """

    @staticmethod
    def create_scene(satname, satnumber, instrument, time_slot, area=None,
                     variant=''):
        """Create a compound satellite scene.
        """

        return GenericFactory.create_scene(satname, satnumber, instrument,
                                           time_slot, None, area, variant)


class PolarFactory(object):

    """Factory for polar satellite scenes.
    """

    @staticmethod
    def create_scene(satname, satnumber, instrument, time_slot, orbit=None,
                     area=None, variant=''):
        """Create a compound satellite scene.
        """

        return GenericFactory.create_scene(satname, satnumber, instrument,
                                           time_slot, orbit, area, variant)


class GenericFactory(object):

    """Factory for generic satellite scenes.
    """

    @staticmethod
    def create_scene(satname, satnumber, instrument, time_slot, orbit,
                     area=None, variant='', end_time=None):
        platform_name = satname + satnumber


class Compositer(scene):

    def __init__(self, scene):
        self.scene = scene

    def __getattr__(self, name):
        # fixme: needs to be callable
        self.scene.compute([name])
        from satpy.writers import get_enhanced_image
        return get_enhanced_image(self.scene[name])


class Scene(satpy.scene.Scene):

    def __init__(self, *args, **kwargs):
        satpy.scene.Scene.__init__(self, *args, **kwargs)

        self.image = Compositer(weakref.proxy(self))
