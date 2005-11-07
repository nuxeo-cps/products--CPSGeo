# -*- coding: ISO-8859-15 -*-
# Copyright (c) 2004 Sean C. Gillies
# Copyright (c) 2005 Nuxeo SARL <http://nuxeo.com>

# Authors : Sean Gillies <sgillies@frii.com>
#           Julien Anguenot <ja@nuxeo.com>

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

"""Web Map Context (WMC)

Specification can be found over there :
https://portal.opengeospatial.org/files/?artifact_id=8618

"""

import lxml.etree

context_ns_uri = 'http://www.opengis.net/context'
context_schemas_uri = 'http://schemas.opengis.net/context/1.0.0/context.xsd'

def WMCElement(tag):
    """WMC based element
    """
    return lxml.etree.Element("{%s}"%context_ns_uri + tag)

class MapContext:
    """ Map Context abstraction

    It uses a Map representation as input and export it as as map
    context
    """

    def __init__(self, map_):
        self._map = map_

    def _getRootElement(self):
        root = WMCElement('ViewContext')
        attrs = {
            '{http://www.w3.org/2001/XMLSchema-instance}schemaLocation':
            context_ns_uri + ' ' + context_schemas_uri,
            'id' : self._map.id,
            'version' : '1.0.0',
            }
        for k, v in attrs.items():
            root.attrib[k] = v
        return root

    def _getGeneralElement(self):
        general = WMCElement('General')
        general.append(self._getWindowElement())
        general.append(self._getBoundingBoxElement())
        return general

    def _getWindowElement(self):
        window = WMCElement('Window')
        window.attrib['width'] = str(self._map.size[0])
        window.attrib['height'] = str(self._map.size[1])
        return window

    def _getBoundingBoxElement(self):
        bbox = WMCElement('BoundingBox')
        bbox.attrib['SRS'] = str(self._map.srs.split()[0])
        bbox.attrib['minx'] = str(self._map.bounds[0])
        bbox.attrib['miny'] = str(self._map.bounds[1])
        bbox.attrib['maxx'] = str(self._map.bounds[2])
        bbox.attrib['maxy'] = str(self._map.bounds[3])
        return bbox

    def _getLayerListElement(self):
        layerlist = WMCElement('LayerList')
        layering = zip(self._map.layernames, self._map.layertitles)

        # mapbuilder draws layers in bottom-top order
        for name, title in layering:

            # Layer
            layer = WMCElement('Layer')
            layer.attrib['queryable'] = '0'
            layer.attrib['hidden'] = str(
                int(name not in self._map.visible_layers))

            # Server
            server = WMCElement('Server')
            server.attrib['service'] = 'OGC:WMS'
            server.attrib['version'] = '1.1.1'
            server.attrib['title'] = 'OGC:WMS'

            # OnlineRessource
            oressource = WMCElement('OnlineResource')
            oressource.attrib[
                '{http://www.w3.org/1999/xlink}type'] = 'simple'
            oressource.attrib[
                '{http://www.w3.org/1999/xlink}href'] = self._map.url
            server.append(oressource)
            layer.append(server)

            # Name
            e_name = WMCElement('Name')
            e_name.text = name
            layer.append(e_name)

            # Title
            e_title = WMCElement('Title')
            e_title.text = title
            layer.append(e_title)

            # Format
            formatlist = WMCElement('FormatList')
            format = WMCElement('Format')
            format.attrib['current'] = '1'
            format.text = self._map.format
            formatlist.append(format)
            layer.append(formatlist)
            layerlist.append(layer)

        return layerlist

    def _getOnlineRessource(self):
        

    def __call__(self):
        """Export self._map to WMC
        """
        wmc_doc_tree = self._getRootElement()
        wmc_doc_tree.append(self._getGeneralElement())
        wmc_doc_tree.append(self._getLayerListElement())
        return lxml.etree.tostring(wmc_doc_tree)

def mapToWebMapContext(map):
    """Helper
    """
    return MapContext(map)()
