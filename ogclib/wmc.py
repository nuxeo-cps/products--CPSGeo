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

class WMCError(Exception):
    """Base class for WMC errors
    """
    pass

def WMCElement(tag):
    """WMC based element
    """
    return etree.Element("{%s}"%context_ns_uri + tag)

class MapContext:
    """ Map Context abstraction

    It uses a Map representation as input and export it as as map
    context
    """

    def __init__(self, map_, **kw):
        """Construct a MapContext instance from a Map instance

        kws contains properties that will he taken into account to
        generate the WMC. Those override the default properties of the
        Map instance.
        """
        self._map = map_
        self._kw = kw

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
        """Construct the Window element defining the size of the map.

        size is extracted from the map instance except if they have
        been passed explicitly at MapContext constuction time
        """
        window = WMCElement('Window')

        if self._kw.get('size'):
            size = self._kw.get('size').split()
        else:
            size = self._map.size

        # example : (800, 600)
        try:
            assert len(size) == 2
        except AssertionError:
            raise WMCError("%s is a wrong size format"%str(size))

        window.attrib['width'] = str(size[0])
        window.attrib['height'] = str(size[1])

        return window

    def _getBoundingBoxElement(self):
        """Construct the bounding box element

        bounds and SRS are extracted from the map instance except if
        they have been passed explicitly at MapContext constuction time
        """

        bbox = WMCElement('BoundingBox')

        if self._kw.get('SRS'):
            srs = self._kw.get('SRS')
        else:
            srs = self._map.srs
            
        try:
            # example : EPSG:4326
            assert len(srs.split(':')) == 2
        except AssertionError:
            raise WMCError("%s is a wrong SRS format"%str(srs))

        bbox.attrib['SRS'] = srs

        if self._kw.get('bounds'):
            bounds = self._kw.get('bounds').split()
        else:
            bounds = self._map.bounds

        try:
            assert len(bounds) == 4
        except AssertionError:
            raise WMCError("%s is a wrong bounds format"%str(bounds))

        bbox.attrib['minx'] = str(bounds[0])
        bbox.attrib['miny'] = str(bounds[1])
        bbox.attrib['maxx'] = str(bounds[2])
        bbox.attrib['maxy'] = str(bounds[3])

        return bbox

    def _getLayerListElement(self):
        layerlist = WMCElement('LayerList')
        layering = zip(self._map.layernames, self._map.layertitles)
        layer_infos = self._map.getLayerInfos()

        # mapbuilder draws layers in bottom-top order
        for name, title in layering:

            # Layer
            layer = WMCElement('Layer')
            layer.attrib['queryable'] = '0'
            layer.attrib['hidden'] = str(
                int(name not in self._map.visible_layers))

            # Layer styles
            if layer_infos and layer_infos.get(title):
                stylelist = WMCElement('StyleList')
                # Get wms `Style` nodes for a given layer
                for e_style in layer_infos.get(title):
                    e_style.attrib['current'] = '1'
                    # Change namespace to wmc
                    for node in e_style.getiterator():
                        tag_name = node.tag[node.tag.rfind('}')+1:]
                        node.tag = "{%s}"%context_ns_uri + tag_name
                    stylelist.append(e_style)
                layer.append(stylelist)

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

    def __call__(self):
        """Export self._map to WMC
        """
        wmc_doc_tree = self._getRootElement()
        wmc_doc_tree.append(self._getGeneralElement())
        wmc_doc_tree.append(self._getLayerListElement())
        return etree.tostring(wmc_doc_tree)

class AggregateMapContext(MapContext):
    """ Map Context abstraction

    It uses a Map representation as input and export it as as map
    context -- with aggregation of all selected layers accomplished through
    overload of the Layer/Name property
    """

    def _getLayerListElement(self):
        layerlist = WMCElement('LayerList')

        # Layer
        layer = WMCElement('Layer')
        layer.attrib['queryable'] = '0'
        layer.attrib['hidden'] = '0'

        # Server
        server = WMCElement('Server')
        server.attrib['service'] = 'OGC:WMS'
        server.attrib['version'] = '1.1.1'
        server.attrib['title'] = 'OGC:WMS'

        # OnlineRessource
        oressource = WMCElement('OnlineResource')
        oressource.attrib['{http://www.w3.org/1999/xlink}type'] = 'simple'
        oressource.attrib['{http://www.w3.org/1999/xlink}href'] = self._map.url
        server.append(oressource)
        layer.append(server)

        # Name
        e_name = WMCElement('Name')
        e_name.text = ','.join(self._map.visible_layers)
        layer.append(e_name)

        # Title
        e_title = WMCElement('Title')
        e_title.text = 'Aggregate Layers'
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

def mapToWebMapContext(map, aggregate_layers=False, kws=None):
    """Helper

    if the second argument evaluates to True, then all map layers are
    aggregated into a single map context layer.

    kws contains parameters to use intead of the default ones from the
    Map instance within the tool (i.e : such as bounds, size, etc...)
    """
    if kws is None:
        kws = {}
    if aggregate_layers:
        return AggregateMapContext(map, **kws)()
    else:
        return MapContext(map, **kws)()

