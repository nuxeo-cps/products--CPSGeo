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
return results

#brainsToGeoRSS(context.title, context.absolute_url(), context.getContent().results)
#container.REQUEST.RESPONSE.setHeader('Content-type', 'text/xml')
#return context.portal_maps.brainsToGeoRSS(context.title, context.absolute_url(), context.getContent().results)



