##parameters=key=None
#$Id$
"""Return the list of all registred map ids within the map repository

Used within a Method vocabularies
"""

# XXX not tested

search = context.search(query={'portal_type':['Map']})

returned = []

for brain in search:
    ob = brain.getObject()
    returned.append(ob.getId())

if key is not None:
    for each in returned:
        if each == key:
            return each

return returned
