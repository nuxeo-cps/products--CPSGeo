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
# $Id$

""" CPS Geo Widget definitions
"""

from Globals import InitializeClass

from Products.CPSSchemas.Widget import CPSWidget, CPSWidgetType
from Products.CPSSchemas.WidgetTypesTool import WidgetTypeRegistry

class CPSMapWidget(CPSWidget):
    """CPS Map Widget
    """

    meta_type = 'CPS Map Widget'

    def prepare(self, datastructure, **kw):
        """Prepare datastructure from datamodel."""
        datamodel = datastructure.getDataModel()
        # XXX check if you need this.

    def validate(self, datastructure, **kw):
        """Validate datastructure and update datamodel.
        """
        # XXX implements me !
        return True

    def render(self, mode, datastructure, **kw):
        """Render in mode from datastructure
        """
        render_method = 'widget_cps_mapdocument'
        meth = getattr(self, render_method, None)

        if meth is None:
            raise RuntimeError("Unknown Render Method %s for widget type %s"
                               % (render_method, self.getId()))

        infos = {}

        # XXX here build the dict containing parameters you will use
        # within your zpt widget to render the map.
        
        return meth(mode=mode, datastructure=datastructure, **infos)

InitializeClass(CPSMapWidget)

class CPSMapWidgetType(CPSWidgetType):
    """CPS Map Widget Type
    """
    meta_type = 'CPS Map Widget Type'
    cls = CPSMapWidget

WidgetTypeRegistry.register(CPSMapWidgetType, CPSMapWidget)
