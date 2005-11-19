# -*- coding: ISO-8859-15 -*-
# Copyright (c) 2005 Nuxeo SARL <http://nuxeo.com>

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
# $Id: CPSPortlet.py 26680 2005-09-09 14:22:18Z janguenot $
"""Allow modules within CPSGeo scope.

PCL/referencing lib defined as externals within CPSGeo.
"""

from AccessControl import allow_module
from AccessControl import allow_class 
    
from cartography.referencing.srs import SpatialReference
from cartography.referencing.transform.proj4 import ProjTransform

allow_module('cartography.referencing.srs')
allow_module('cartography.referencing.transform.proj4')

allow_class(SpatialReference)
allow_class(ProjTransform)