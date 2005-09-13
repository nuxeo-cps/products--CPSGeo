##parameters=
"""The CPSGeo geolocation schema promotes CPS Documents to the status of
lightweight GIS features
"""

geolocation_schema = {
    'spatial_reference_system': {
        'type': 'CPS String Field',
        'data': {
            'default_expr': 'string:EPSG:4326',
            'is_searchabletext': 0,
            'acl_read_permissions': '',
            'acl_read_roles': '',
            'acl_read_expr': '',
            'acl_write_permissions': '',
            'acl_write_roles': '',
            'acl_write_expr': '',
            'read_ignore_storage': 0,
            'read_process_expr': '',
            'read_process_dependent_fields': [],
            'write_ignore_storage': 0,
            'write_process_expr': '',
        },
    },
    'pos_list_dimension': {
        'type': 'CPS Int Field',
        'data': {
            'default_expr': 'python:2',
            'is_searchabletext': 0,
            'acl_read_permissions': '',
            'acl_read_roles': '',
            'acl_read_expr': '',
            'acl_write_permissions': '',
            'acl_write_roles': '',
            'acl_write_expr': '',
            'read_ignore_storage': 0,
            'read_process_expr': '',
            'read_process_dependent_fields': [],
            'write_ignore_storage': 0,
            'write_process_expr': '',
        },
    },
    'pos_list': {
        'type': 'CPS String Field',
        'data': {
            'default_expr': 'string:',
            'is_searchabletext': 0,
            'acl_read_permissions': '',
            'acl_read_roles': '',
            'acl_read_expr': '',
            'acl_write_permissions': '',
            'acl_write_roles': '',
            'acl_write_expr': '',
            'read_ignore_storage': 0,
            'read_process_expr': '',
            'read_process_dependent_fields': [],
            'write_ignore_storage': 0,
            'write_process_expr': '',
        },
    },
}

dict = {}
dict['geolocation'] = geolocation_schema
return dict

