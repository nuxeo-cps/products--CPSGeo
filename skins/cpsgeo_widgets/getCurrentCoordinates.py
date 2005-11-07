##parameters=
""" Return the coordinate of the context.

If it's not set then return 0.0,0.0 as default value.

$Id: $
"""

pos_list = getattr(context.getContent(), 'pos_list', False)
if pos_list:
    return pos_list.replace(' ',',')
return '0.0,0.0'

