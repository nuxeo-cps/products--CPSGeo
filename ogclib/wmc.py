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

import lxml.etree

def WMCElement(tag):
    """WMC based element
    """
    return lxml.etree.Element("{http://www.opengis.net/context}" + tag)

def mapToWebMapContext(map):
    """Export a Web Map Context document from a Map
    """
    e_context = WMCElement('ViewContext')
    e_context.attrib['{http://www.w3.org/2001/XMLSchema-instance}schemaLocation'] = 'http://www.opengis.net/context http://schemas.opengis.net/context/1.0.0/context.xsd'
    e_context.attrib['id'] = map.id
    e_context.attrib['version'] = '1.0.0'
    e_general = WMCElement('General')
    e_window = WMCElement('Window')
    e_window.attrib['width'] = str(map.size[0])
    e_window.attrib['height'] = str(map.size[1])
    e_general.append(e_window)
    e_bbox = WMCElement('BoundingBox')
    e_bbox.attrib['SRS'] = str(map.srs.split()[0])
    e_bbox.attrib['minx'] = str(map.bounds[0])
    e_bbox.attrib['miny'] = str(map.bounds[1])
    e_bbox.attrib['maxx'] = str(map.bounds[2])
    e_bbox.attrib['maxy'] = str(map.bounds[3])
    e_general.append(e_bbox)
    e_context.append(e_general)
    e_layerlist = WMCElement('LayerList')
    layering = zip(map.layernames, map.layertitles)
    # mapbuilder draws layers in bottom-top order
    for name, title in layering:
        e_layer = WMCElement('Layer')
        e_layer.attrib['queryable'] = '0'
        e_layer.attrib['hidden'] = str(int(name not in map.visible_layers))
        e_server = WMCElement('Server')
        e_server.attrib['service'] = 'OGC:WMS'
        e_server.attrib['version'] = '1.1.1'
        e_server.attrib['title'] = 'OGC:WMS'
        e_url = WMCElement('OnlineResource')
        e_url.attrib['{http://www.w3.org/1999/xlink}type'] = 'simple'
        e_url.attrib['{http://www.w3.org/1999/xlink}href'] = map.url
        e_server.append(e_url)
        e_layer.append(e_server)
        e_name = WMCElement('Name')
        e_name.text = name
        e_layer.append(e_name)
        e_title = WMCElement('Title')
        e_title.text = title
        e_layer.append(e_title)
        e_formatlist = WMCElement('FormatList')
        e_format = WMCElement('Format')
        e_format.attrib['current'] = '1'
        e_format.text = map.format
        e_formatlist.append(e_format)
        e_layer.append(e_formatlist)
        e_layerlist.append(e_layer)
    e_context.append(e_layerlist)
    return lxml.etree.tostring(e_context)

    
