##parameters=key=None
#$Id$
"""Return the list of all registred map ids within the map repository

Used within a Method vocabularies
"""

maptool = context.portal_maps

returned = []
for id_, map_ in maptool.items():
    label = id_ \
            + ' -- ' \
            + getattr(map_, 'name', '') \
            + ' ( ' \
            + getattr(map_, 'url', 'UNKNOWN') \
            +  ' ) '
    returned.append((id_, label))

if key is not None:
    for each in returned:
        if each[0] == key:
            return each[0]

return returned
