# $Id$

# =============================================================================
# Cartographic Objects for Zope. Copyright (C) 2004 Sean C. Gillies
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA 02111-1307 USA
#
# Contact email: sgillies@frii.com
# =============================================================================

# The georss module currently "lives" in ZCO, but may soon be split out into
# a separate package

from cartography.referencing.srs import SpatialReference
from cartography.referencing.transform.proj4 import ProjTransform

from Products.CPSGeo import etree

# Convenience wrappers for the Element factory
# --------------------------------------------
def RDFElement(tag):
    return etree.Element(
        "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}" + tag)

def RSSElement(tag):
    return etree.Element(
        "{http://purl.org/rss/1.0/}" + tag)

def TAXOElement(tag):
    return etree.Element(
        "{http://purl.org/rss/1.0/modules/taxonomy/}" +e.tag)

def DCElement(tag):
    return etree.Element(
        "{http://purl.org/dc/elements/1.1/}" + tag)

def SYNElement(tag):
    return etree.Element(
        "{http://purl.org/rss/1.0/modules/syndication/}" + tag)

def GEOElement(tag):
    return etree.Element(
        "{http://www.w3.org/2003/01/geo/wgs84_pos#}" + tag)

def brainsToGeoRSS(title, about, brains, srs):
    """Convert catalog query result brains to GeoRSS format
    
    We expect the following brain attributes:
    - Title
    - Description
    - getURL
    - Date
    - pos_list
    
    """
    rdf = RDFElement('RDF')
    channel = RSSElement('channel')
    channel.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about'] \
                  = about
    chtitle = RSSElement('title')
    chtitle.text = 'CPS Geo Documents'
    channel.append(chtitle)
    chlink = RSSElement('link')
    chlink.text = about
    channel.append(chlink)
    chperiod = SYNElement('updatePeriod')
    chperiod.text = 'often'
    chfreq = SYNElement('updateFrequency')
    chfreq.text = '1'
    channel.append(chperiod)
    channel.append(chfreq)
    chitems = RSSElement('items')
    seq = RDFElement('Seq')
    for schema in brains:
        li = RDFElement('li')
        li.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource'] = schema.getURL()
        seq.append(li)
    chitems.append(seq)
    channel.append(chitems)
    rdf.append(channel)
    
    # transform geo-locations from WGS84 (stored form) to the map SRS
    locations = []
    for schema in brains:
        pos_list = schema.pos_list
        if pos_list:
            x, y = pos_list.strip().split()
            locations.append((float(x), float(y)))
    wgs84 = SpatialReference(epsg=4326)
    map_srs = SpatialReference(epsg=int(srs.split(':')[1]))
    t = ProjTransform(map_srs, wgs84)
    map_locations = t.transform(locations)
    
    for schema, map_location in zip(brains, map_locations):
        item = RSSElement('item')
        item.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about'] \
                   = schema.getURL()
        title = RSSElement('title')
        title.text = schema.Title
        item.append(title)
        link = RSSElement('link')
        link.text = schema.getURL()
        item.append(link)
        description = RSSElement('description')
        description.text = schema.Description or '-- no description --'
        item.append(description)
        date = DCElement('date')
        date.text = schema.Date
        item.append(date)
        
        # location
        long = GEOElement('long')
        long.text = str(map_location[0])
        lat = GEOElement('lat')
        lat.text = str(map_location[1])
        item.append(long)
        item.append(lat)
        rdf.append(item)

    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' \
           + etree.tostring(rdf)

