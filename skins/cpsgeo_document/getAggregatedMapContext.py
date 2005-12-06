##parameters=REQUEST=None
"""Return a WMC document

$Id$
"""
return context.getContent().getWebMapContext(True, REQUEST=REQUEST)
