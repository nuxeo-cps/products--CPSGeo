## Script (Python) "getCurrentCoordinates"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

pos_list = getattr(context.getContent(), 'pos_list', False)
if pos_list:
    return pos_list.replace(' ',',')
else:
    return '0.0,0.0'

