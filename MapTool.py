# (C) Copyright 2003 Nuxeo SARL <http://nuxeo.com>
# Author: Florent Guillaume <fg@nuxeo.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#
# $Id$
"""Map Tool
"""

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from Products.CMFCore.utils import UniqueObject
from OFS.Folder import Folder

from Map import Map


class MapPoolError(Exception):

    """Errors involving a Tool's pool of maps"""
    
    
class MapTool(UniqueObject, Folder):

    """Map Tool
    """

    meta_type = 'CPS Map Tool'

    security = ClassSecurityInfo()

    def __init__(self):
        """Initialize"""
        self.id = 'portal_maps'
        self._maps = {}

    def addMap(self, id, url):
        """Add a map"""
        if id not in self._maps.keys():
            self._maps[id] = url
        else:
            raise MapPoolError, \
            "A map exists with id: %s" % (id)
        
        
InitializeClass(MapTool)
