## Script (Python) "getGeoRSSModel"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

from Products.CPSGeo.georss import brainsToGeoRSS

results = context.getContent().results
brains = []
for r in results:
    brain = context.portal_catalog(path=r)
    brains.append(brain)
container.REQUEST.RESPONSE.setHeader('Content-type', 'text/xml')
return brainsToGeoRSS(context.title, context.absolute_url(), brains)

