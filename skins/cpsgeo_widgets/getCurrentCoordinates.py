## Script (Python) "getCurrentCoordinates"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

pos_list = context.getContent().pos_list
if pos_list:
    return pos_list.replace(' ',',')
else:
    return '0.0,0.0'

