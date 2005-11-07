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

import urllib
import lxml.etree

class WMSError(Exception):
    """Base class for WMS module errors
    """

    def __init__(self, message):
        """Initialize a WMS Error"""
        self.message = message

    def toxml(self):
        """Serialize into a WMS Service Exception XML
        """
        preamble = '<?xml version="1.0" ?>'
        report_elem = lxml.etree.Element('ServiceExceptionReport')
        report_elem.attrib['version'] = '1.1.1'
        # Service Exception
        exception_elem = lxml.etree.Element('ServiceException')
        exception_elem.text = self.message
        report_elem.append(exception_elem)
        return preamble + lxml.etree.tostring(report_elem)

class WebMapService:
    """x
    """
    def capabilities_xml(self):
        """x
        """
        top = lxml.etree.Element('a')
        top.text = self.getName()
        return lxml.etree.tostring(top)

class WMSCapabilitiesInfoset:
    """High-level container for WMS Capabilities based on lxml.etree
    """
    
    def __init__(self, infoset):
        """Initialize"""
        self._infoset = infoset

    def getroot(self):
        return self._infoset

    def getservice(self):
        return self._infoset.find('Service')
       
    def servicename(self):
        e_service = self.getservice()
        return e_service.find('Name').text

    def servicetitle(self):
        e_service = self.getservice()
        return e_service.find('Title').text

    def getmapformats(self):
        e_getmap = self._infoset.find('Capability/Request/GetMap')
        formats = ()
        for f in e_getmap.getiterator('Format'):
            formats = formats + (f.text,)
        return formats
   
    def layersrs(self):
        e_layer = self._infoset.find('Capability/Layer')
        srs = ()
        for s in e_layer.getiterator('SRS'):
            srs = srs + (s.text,)
        return srs

    def layernames(self):
        names = ()
        for n in self._infoset.findall('Capability/Layer/Layer/Name'):
            names = names + (n.text,)
        return names
 
    def layertitles(self):
        titles = ()
        for n in self._infoset.findall('Capability/Layer/Layer/Title'):
            titles = titles + (n.text,)
        return titles

    def layerlegendURLs(self):
        legendURLs = ()
        for each in self._infoset.findall(
            'Capability/Layer/Layer/Style/LegendURL/OnlineResource'):
            href_ = each.attrib['{http://www.w3.org/1999/xlink}href']
            legendURLs += (href_,)
        return legendURLs

class WMSCapabilitiesReader:
    """Read and parse capabilities document into a lxml.etree infoset
    """

    def __init__(self, version='1.1.1'):
        """Initialize"""
        self.version = version
        self._infoset = None
       
    def capabilities_url(self, service_url):
        """Return a capabilities url
        """
        if service_url.find('?') < 0:
            return '%s?service=WMS&version=%s&request=GetCapabilities' \
                    % (service_url, self.version)
        if service_url.find('?') >= 0:
            return service_url
        
    def read(self, service_url):
        """Get and parse a WMS capabilities document, returning an
        instance of WMSCapabilitiesInfoset

        service_url is the base url, to which is appended the service,
        version, and request parameters
        """
        request = self.capabilities_url(service_url)
        u = urllib.urlopen(request)
        return WMSCapabilitiesInfoset(
            lxml.etree.fromstring(u.read()))

