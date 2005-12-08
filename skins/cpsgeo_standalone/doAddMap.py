##parameters=url='', REQUEST=None
"""Add a new map given an URL

$Id$
"""

mtool = context.portal_maps
id_ = mtool.addMap(url)
if id_ and REQUEST:
    url = context.absolute_url() + \
          '/cps_map_edit' + \
          '?mappath=portal_maps/%s'%id_
    return REQUEST.RESPONSE.redirect(url)
