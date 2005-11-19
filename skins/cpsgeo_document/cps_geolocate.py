##parameters=REQUEST=None
"""geo locate a document

$Id$
"""

from cartography.referencing.srs import SpatialReference
from cartography.referencing.transform.proj4 import ProjTransform

if REQUEST is not None:

    form = REQUEST.form

    pos_list = ""
    if form.has_key('pos_list'):
        pos_list = form['pos_list']

    # XXX your customer's default value
    # the correct value needs to reach this method. see submit_location()
    # in cps_geo_common.js -- Sean
    srs = "epsg:27582"
    if form.has_key('srs'):
        srs = form['srs']
        
    # transform coordinates from map reference system to WGS84
    code = int(srs.split(':')[1])
    t = ProjTransform(SpatialReference(epsg=4326), SpatialReference(epsg=code))
    x, y = [float(v) for v in pos_list.split()]
    [(m, n)] = t.transform([(x, y)])
    
    # Update metadata
    context.getContent().edit(pos_list='%f %f' % (m, n))

    psm = 'psm_document_geolocated'
    redirect_url = context.absolute_url() + \
                   '?portal_status_message=' + \
                   psm
    return REQUEST.RESPONSE.redirect(redirect_url)
