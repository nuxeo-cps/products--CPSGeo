##parameters=
#$Id$
"""
Return the body onload attribute content
"""

request = container.REQUEST

if request.has_key('URL'):
    URL = container.REQUEST['URL']
    if URL is not None and \
        (URL.endswith('search_form') or URL.endswith('advanced_search_form')):
        return 'highlightSearchTerm();setFocus();'
    # XXX condition
    return 'mbDoLoad();switch_map();'

return 'setFocus();'
