## Script (Python) "getCurrentCoordinates"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
obid = context.id
path = '/'.join(context.getPhysicalPath())
results = container.portal_catalog(path=path, getId=obid)
if results:
    pos = getattr(results[0], 'pos_list', '0 0')
    return '%s,%s' % tuple(results[0].pos_list.split())
else:
    return '0 0'
