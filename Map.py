# (C) Copyright 2005 Nuxeo SARL <http://nuxeo.com>
# Author: Sean Gillies (sgillies@frii.com)
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
"""Map
"""

from Products.CMFCore.PortalContent import PortalContent

class Map(PortalContent):

    """Map
    """

    def __init__(self, url, name='', title='', version='',
                 bounds=[], srs=[], layers=[], formats=[]):
        """Initialize"""
        self.url = url
        self.name = name
        self.title = title
        self.version = version
        self.bounds = bounds
        self.srs = srs
        self.layers = layers
        self.formats = formats
        

