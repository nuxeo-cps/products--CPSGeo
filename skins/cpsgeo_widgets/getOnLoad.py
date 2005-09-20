## Script (Python) "getOnLoad"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
#$Id: getOnLoad.py 7215 2005-03-03 13:58:20Z sfermigier $
"""
Return the body onload attribute content
"""

request = container.REQUEST

if request.has_key('URL'):
    URL = container.REQUEST['URL']
    if URL is not None and \
        (URL.endswith('search_form') or URL.endswith('advanced_search_form')):
        return 'highlightSearchTerm();setFocus();'
    if (URL is not None and
        URL.endswith('cpsmap_document_view') or
        URL.endswith('cps_geolocation_form') or
        URL.endswith('cps_map_server')
        ):
        return 'mbDoLoad(); switch_map()'
return ''
