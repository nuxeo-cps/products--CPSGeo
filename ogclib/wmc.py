# $Id: DataStore.py 41 2005-05-19 21:40:47Z sgillies $

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

# try to find elementtree or lxml
try:
    import elementtree
    from elementtree.ElementTree import Element, SubElement
    from elementtree.ElementTree import tostring, fromstring
    # Monkey Patch adds to the default well known namespaces
    elementtree.ElementTree._namespace_map.update({
        "http://www.opengis.net/context":               "wmc",
        "http://www.w3.org/1999/xlink":                 "xlink",
        "http://www.w3.org/2001/XMLSchema-instance":    "xsi"})
except:
    from lxml.etree import Element, SubElement, tostring, fromstring

def WMCElement(tag):
    return Element("{http://www.opengis.net/context}" + tag)
    
