##parameters=key=None
#$Id$
"""Return the list of all registred map ids within the map repository

Used within a Method vocabularies
"""

from zLOG import LOG, DEBUG
LOG("CPSGeo Voc", DEBUG, key)

maptool = context.portal_maps

returned = []
for id_, map_ in maptool.items():
    label = id_ \
            + ' ( ' \
            + getattr(map_, 'title', 'UNKNOWN') \
            +  ' ) '
    returned.append((id_, label))

if key is not None:
    for each in returned:
        if each[0] == key:
            return each[1]
    return ''

return returned
