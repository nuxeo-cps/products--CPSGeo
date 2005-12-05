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
# $Id: CPSPortlet.py 26680 2005-09-09 14:22:18Z janguenot $

import os
import sys

import unittest
import CPSGeoTestCase

class MapTest(CPSGeoTestCase.CPSGeoTestCase):

    def afterSetUp(self):
        self.login('manager')
        self._mtool = self.portal.portal_maps

        members = self.portal.portal_directories.members
        # Create a Member
        members.createEntry(
            {'id': 'member', 'givenName' : 'Foo',
             'sn': 'Bar', 'roles': ['Member']})
        self.portal.portal_membership.createMemberArea('member')

    def beforeTearDown(self):
        self.logout()

    def testMapTool(self):
        self.assertEquals(self._mtool.meta_type, 'CPS Map Tool')

    def testAddMap(self):

        id_ = 'map1'
        url = 'http://wms.jpl.nasa.gov/wms.cgi'
        self._createMap(id_, url)

        self.assertEquals(self._mtool.mapContexts(),
                          [{'id': 'map1',
                            'title': 'JPL World Map Service',
                            'path': 'portal_maps/map1/mapContext'}])
        map1 = getattr(self._mtool, 'map1')
        self.assertEquals(map1.name, 'OGC:WMS')
        self.assertEquals(map1.title, 'JPL World Map Service')
        map1.srs = 'EPSG:4326'
        map1.format = 'image/jpeg'
        map1.bounds = (-120,25,-80,55)
        map1.size = (400,300)
        map1.visible_layers = ('global_mosaic',)
        xml = self._mtool.map1.mapContext()
        f = open('testAddMap.xml', 'w')
        f.write(xml)
        f.close()
        os.system('rm -f testAddMap.xml')

    def test_mapVocabularyNoKey(self):

        maps = self.portal.getAllMapIds()
        self.assert_(not maps)

        id_ = 'map1'
        url = 'http://wms.jpl.nasa.gov/wms.cgi'
        self._createMap(id_, url)

        maps = self.portal.getAllMapIds()
        self.assertEqual(len(maps), 1)
        map_ = self._mtool.map1

        self.assertEqual(maps[0][0], 'map1')
        self.assertEqual(maps[0][1], map_.title)

    def test_mapVocabularyKey(self):

        maps = self.portal.getAllMapIds()
        self.assert_(not maps)

        id_ = 'map1'
        url = 'http://wms.jpl.nasa.gov/wms.cgi'
        self._createMap(id_, url)
        map_ = self._mtool.map1

        map_info_ = self.portal.getAllMapIds('map1')
        self.assertEqual(map_info_, map_.title)

    def test_getCoordinatesForAsManager(self):

        default_ = '0.0,0.0'

        # No coordinates for now
        self.assertEqual(
            self._mtool.getCoordinatesFor(self.portal.workspaces), default_)

        # Set coordinates for the workspaces
        self.portal.workspaces.getContent().pos_list = '1 2'
        self.assertEqual(
            self._mtool.getCoordinatesFor(self.portal.workspaces), '1,2')

    def test_wrong_getCoordinates(self):

        # Set coordinates for the workspaces
        self.portal.workspaces.getContent().pos_list = ' 1 \n 2 \t'
        self.assertEqual(
            self._mtool.getCoordinatesFor(self.portal.workspaces), '1,2')

    def test_getCoordinatesForAsMember(self):

        self.login('member')

        default_ = '0.0,0.0'

        # No allowed so the user will get 0.0 instead of the real
        # coordinates instead of the real one.
        self.assertEqual(
            self._mtool.getCoordinatesFor(self.portal.workspaces), default_)

        # No coordinates
        self.assertEqual(
            self._mtool.getCoordinatesFor(
            self.portal.workspaces.members.member), default_)

        # Set coordinates for the workspaces
        self.portal.workspaces.members.member.getContent().pos_list = '1 2'
        self.assertEqual(
            self._mtool.getCoordinatesFor(
            self.portal.workspaces.members.member), '1,2')

        self.logout()

    #
    # PRIVATE
    #

    def _createMap(self, id_, url, **kw):
        return self._mtool.manage_addMap(id=id_, url=url)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(MapTest))
    return suite

if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
