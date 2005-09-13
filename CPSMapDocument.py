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

"""CPS Map Document
"""

from Globals import InitializeClass

from Products.CPSDocument.CPSDocument import CPSDocument

class CPSMapDocument(CPSDocument):
    """CPS Map Document
    """
    meta_type = 'CPS Map Document'
    portal_type = meta_type

    # XXX implement me !

InitializeClass(CPSMapDocument)

def addCPSMapDocument(container, id, REQUEST=None, **kw):
    """Add a CPS Map Document
    """
    ob = CPSMapDocument(id, **kw)
    container._setObject(id, ob)
    if REQUEST:
        ob = container._getOb(id)
        REQUEST.RESPONSE.redirect(ob.absolute_url()+'/manage_main')
