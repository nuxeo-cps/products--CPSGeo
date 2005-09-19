##parameters=REQUEST=None
"""geo locate a document

$Id$
"""

if REQUEST is not None:
    form = REQUEST.form
    pos_list = form['pos_list']
    context.getContent().edit(pos_list=pos_list)

    psm = 'psm_document_geolocated'
    redirect_url = context.absolute_url() + \
                   '?portal_status_message=' + \
                   psm
    return REQUEST.RESPONSE.redirect(redirect_url)
