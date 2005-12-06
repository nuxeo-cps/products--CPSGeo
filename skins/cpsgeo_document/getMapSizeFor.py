##parameters=map_id=''
"""Return the map size given a map id

$Id$
"""

mtool = context.portal_maps
if mtool.has_key(map_id):
    return ' '.join(map(str, mtool[map_id].size))
return ''
