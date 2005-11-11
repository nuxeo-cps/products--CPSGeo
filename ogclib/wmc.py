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

from Products.CPSGeo import etree

context_ns_uri = 'http://www.opengis.net/context'
context_schemas_uri = 'http://schemas.opengis.net/context/1.0.0/context.xsd'

def WMCElement(tag):
    """WMC based element
    """
    return etree.Element("{%s}"%context_ns_uri + tag)

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
    #
    # Notes: Nuxeo's mapping customer seems to want a single layer in the
    # mapbuilder client application. The best way to do that is to have a 
    # single Layer element in the LayerList and join the external WMS layer
    # names like:
    # 
    # <Layer>
    #   <Name>layer_1,layer_2,layer_3,...</Name>
    #   ...
    # </Layer>
    #
    # The effect is a single GetMap request to the external WMS for an image
    # with data merged from all the layers
    #
    # -- Sean
    
        layerlist = WMCElement('LayerList')
        #layering = zip(self._map.layernames, self._map.layertitles) 
        # XXX: above is not needed anymore -- Sean
        layer_infos = self._map.getLayerInfos()

        # mapbuilder draws layers in bottom-top order
        #for name, title in layering:
        # XXX: loop over layers is not needed -- Sean

        # Layer
        layer = WMCElement('Layer')
        layer.attrib['queryable'] = '0'
        layer.attrib['hidden'] = '0'
        
        #str(
        #        int(name not in self._map.visible_layers))

        #    # Layer style
        #    if layer_infos and layer_infos.get(title):
        #        stylelist = WMCElement('StyleList')
        #        style = layer_infos.get(title)[0]
        #        stylelist.append(style)
        #        layer.append(stylelist)
        # XXX: a StyleList element no longer has meaning for this aggregate
        # layer -- Sean

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
        e_name.text = ','.join(self._map.visible_layers)
        layer.append(e_name)

        # Title
        e_title = WMCElement('Title')
        e_title.text = 'Aggregate Layer'
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

    def __call__(self):
        """Export self._map to WMC
        """
        wmc_doc_tree = self._getRootElement()
        wmc_doc_tree.append(self._getGeneralElement())
        wmc_doc_tree.append(self._getLayerListElement())
        return etree.tostring(wmc_doc_tree)

def mapToWebMapContext(map):
    """Helper
    """
    return MapContext(map)()
