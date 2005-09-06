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

# try to find elementtree or lxml
try:
    import elementtree
    from elementtree.ElementTree import Element, SubElement
    from elementtree.ElementTree import tostring, fromstring
    # Monkey Patch adds to the default well known namespaces
    elementtree.ElementTree._namespace_map.update({
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#":  "rdf", 
        "http://purl.org/rss/1.0/":                     "rss", 
        "http://purl.org/rss/1.0/modules/taxonomy/":    "taxo", 
        "http://purl.org/dc/elements/1.1/":             "dc", 
        "http://purl.org/rss/1.0/modules/syndication/": "syn", 
        "http://www.w3.org/2003/01/geo/wgs84_pos#":     "geo"})
except:
    from lxml.etree import Element, SubElement, tostring, fromstring


# Convenience wrappers for the Element factory
# --------------------------------------------
def RDFElement(tag):
    return Element("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}" + tag)

def RSSElement(tag):
    return Element("{http://purl.org/rss/1.0/}" + tag)

def TAXOElement(tag):
    return Element("{http://purl.org/rss/1.0/modules/taxonomy/}" +e.tag)

def DCElement(tag):
    return Element("{http://purl.org/dc/elements/1.1/}" + tag)

def SYNElement(tag):
    return Element("{http://purl.org/rss/1.0/modules/syndication/}" + tag)
    return e

def GEOElement(tag):
    return Element("{http://www.w3.org/2003/01/geo/wgs84_pos#}" + tag)


def brainsToGeoRSS(title, about, brains):
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
    rdf.append(channel)
    
    for schema in brains:
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
        description.text = schema.Description
        item.append(description)
        date = DCElement('date')
        date.text = schema.Date
        item.append(date)
        # location
        x, y = schema.pos_list.split()
        long = GEOElement('long')
        long.text = x
        lat = GEOElement('lat')
        lat.text = y
        item.append(long)
        item.append(lat)
        rdf.append(item)

    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' \
           + tostring(rdf)

