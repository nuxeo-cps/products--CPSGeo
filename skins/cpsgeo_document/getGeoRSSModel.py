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

brains = context.getSearchWidgetContents(context.getContent().getDataModel())
container.REQUEST.RESPONSE.setHeader('Content-type', 'text/xml')
return brainsToGeoRSS(context.title, context.absolute_url(), brains)

