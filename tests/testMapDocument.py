# -*- coding: ISO-8859-15 -*-
# Copyright (c) 2005 Nuxeo SARL <http://nuxeo.com>
# Author : Julien Anguenot <ja@nuxeo.com>

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

import os
import unittest

from Testing.makerequest import makerequest

import CPSGeoTestCase

from Products.CPSGeo import etree

class FakeResponse:

    def redirect(self, url):
        return url

    def setHeader(self, x, y):
        setattr(self, x, y)

class CPSMapDocumentTestCase(CPSGeoTestCase.CPSGeoTestCase):

    def afterSetUp(self):
        self.login('manager')
        self._mtool = self.portal.portal_maps
        self._wftool = self.portal.portal_workflow

        members = self.portal.portal_directories.members
        # Create a Member
        members.createEntry(
            {'id': 'member', 'givenName' : 'Foo',
             'sn': 'Bar', 'roles': ['Member']})
        self.portal.portal_membership.createMemberArea('member')

        # Create one map instance within the repository
        id_ = 'map1'
        url = 'http://wms.jpl.nasa.gov/wms.cgi'
        self._createMap(id_, url)

    def beforeTearDown(self):
        self.logout()

    def test_create_map_document(self):

        self.login('manager')
        kws = {
            'Title' : 'A map document',
            'map_id' : 'map1',
            }
        mapdoc = self._createMapDocument(
            self.portal.workspaces, 'mapdoc', **kws)

        self.assert_(mapdoc)
        self.assertEqual(mapdoc.getContent().map_id, 'map1')
        self.assertEqual(mapdoc.getContent()._getMapInstance(),
                         self._mtool['map1'])

    def test_getGeoRSSModel(self):

        self.login('manager')
        kws = {
            'Title' : 'A map document',
            'map_id' : 'map1',
            }
        mapdoc = self._createMapDocument(
            self.portal.workspaces, 'mapdoc', **kws)

        request = makerequest(mapdoc)
        request.RESPONSE = FakeResponse()

        rss = mapdoc.getContent().getGeoRSSModel(mapdoc, REQUEST=request)

        self.assertEqual(getattr(request.RESPONSE, 'Content-type'), 'text/xml')

        expected = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"><rss:channel rdf:about="http://nohost/portal/workspaces/mapdoc" xmlns:rss="http://purl.org/rss/1.0/"><rss:title>CPS Geo Documents</rss:title><rss:link>http://nohost/portal/workspaces/mapdoc</rss:link><syn:updatePeriod xmlns:syn="http://purl.org/rss/1.0/modules/syndication/">often</syn:updatePeriod><syn:updateFrequency xmlns:syn="http://purl.org/rss/1.0/modules/syndication/">1</syn:updateFrequency><rss:items><rdf:Seq /></rss:items></rss:channel></rdf:RDF>"""
        self.assertEqual(str(rss), expected)

    def test_getGeoRSSModelWithDocs(self):

        self.login('manager')
        kws = {
            'Title' : 'A map document',
            'map_id' : 'map1',
            'query_portal_type' : ['Workspace'],
            }
        mapdoc = self._createMapDocument(
            self.portal.workspaces, 'mapdoc', **kws)

        request = makerequest(mapdoc)
        request.RESPONSE = FakeResponse()

        # generate the rss that includes the search results
        rss = mapdoc.getContent().getGeoRSSModel(mapdoc, REQUEST=request)
        self.assertEqual(getattr(request.RESPONSE, 'Content-type'), 'text/xml')

        # XXX test the rdf doc

    def test_getWebMapContext(self):

        self.login('manager')
        kws = {
            'Title' : 'A map document',
            'map_id' : 'map1',
            }
        mapdoc = self._createMapDocument(
            self.portal.workspaces, 'mapdoc', **kws)

        request = makerequest(mapdoc)
        request.RESPONSE = FakeResponse()

        wmc = mapdoc.getContent().getWebMapContext(REQUEST=request)

        self.assertEqual(getattr(request.RESPONSE, 'Content-type'), 'text/xml')
        # XXX test the wmc doc

    def test_getAggWebMapContext(self):

        self.login('manager')
        kws = {
            'Title' : 'A map document',
            'map_id' : 'map1',
            }
        mapdoc = self._createMapDocument(
            self.portal.workspaces, 'mapdoc', **kws)

        request = makerequest(mapdoc)
        request.RESPONSE = FakeResponse()

        request = makerequest(mapdoc)
        request.RESPONSE = FakeResponse()

        wmc = mapdoc.getContent().getWebMapContext(True, REQUEST=request)

        self.assertEqual(getattr(request.RESPONSE, 'Content-type'), 'text/xml')
        # XXX test the wmc doc

    def test_getGeoRSSModelFromURL(self):

        self.login('manager')
        kws = {
            'Title' : 'A map document',
            'map_id' : 'map1',
            }
        mapdoc = self._createMapDocument(
            self.portal.workspaces, 'mapdoc', **kws)

        rss = mapdoc.getGeoRSSModel()

        # XXX test the wmc doc

    def test_getMapContextFromURL(self):

        self.login('manager')
        kws = {
            'Title' : 'A map document',
            'map_id' : 'map1',
            }
        mapdoc = self._createMapDocument(
            self.portal.workspaces, 'mapdoc', **kws)

        rss = mapdoc.getMapContext()

        # XXX test the wmc doc

    def test_getAggregateMapContextFromURL(self):

        self.login('manager')
        kws = {
            'Title' : 'A map document',
            'map_id' : 'map1',
            }
        mapdoc = self._createMapDocument(
            self.portal.workspaces, 'mapdoc', **kws)

        rss = mapdoc.getAggregatedMapContext()

        # XXX test the wmc doc

    #
    # PRIVATE
    #

    def _createMap(self, id_, url, **kw):
        return self._mtool.manage_addMap(id=id_, url=url)

    def _createMapDocument(self, where, id_, **kw):
        this_id = self._wftool.invokeFactoryFor(
            where, 'CPS Map Document', id_, **kw)
        return getattr(where, this_id)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CPSMapDocumentTestCase))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
