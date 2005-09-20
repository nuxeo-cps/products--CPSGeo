##parameters=
"""Return custom layouts types."""

cpsgeo_layout = {
    'widgets': {
        'pos_list': {
            'type': 'String Widget',
            'data': {
                'title': '',
                'fields': ('pos_list',),
                'is_required': False,
                'label': 'label_WGS84_coordinates',
                'label_edit': 'label_WGS84_coordinates',
                'description': '',
                'help':  'A string of location coordinates. A point location must be represented as a x (longitude east of Greenwich meridian) and y (latitude north of equator) pair in decimal degree units. For example: Paris: "2.40 48.7333", or Denver: "-105.0 39.75"',
                'is_i18n': True,
                'readonly_layout_modes': (),
                'hidden_layout_modes': (),
                'hidden_readonly_layout_modes': (),
                'hidden_empty': False,
                'hidden_if_expr': '',
                'css_class': '',
                'widget_mode_expr': '',
                'display_width': 25,
                'size_max': 0,
            },
        },
    },
    'layout': {
        'style_prefix': 'layout_default_',
        'flexible_widgets': (),
        'ncols': 1,
        'rows': [
            [{'widget_id': 'pos_list', 'ncols': 1},
            ],
        ],
    },
}

map_document_layout = {
    'widgets': {
        'map_id': {
            'type': 'Select Widget',
            'data': {
                'title': '',
                'fields': ('map_id',),
                'is_required': True,
                'label': 'label_cpsgeo_map_id',
                'label_edit': 'label_cpsgeo_map_id',
                'description': '',
                'help': '',
                'is_i18n': True,
                'readonly_layout_modes': (),
                'hidden_layout_modes': (),
                'hidden_readonly_layout_modes': (),
                'hidden_empty': False,
                'hidden_if_expr': '',
                'widget_mode_expr': '',
                'css_class': '',
                'css_class_expr': '',
                'javascript_expr': '',
                'vocabulary': 'maps',
                'translated': False,
            },
        },
        'map_rendering': {
            'type': 'Map Widget',
            'data': {
                'title': '',
                'fields': (),
                'is_required': False,
                'label': '',
                'label_edit': '',
                'description': '',
                'help': '',
                'is_i18n': False,
                'readonly_layout_modes': (),
                'hidden_layout_modes': ('create', 'edit', 'metadata'),
                'hidden_readonly_layout_modes': (),
                'hidden_empty': False,
                'hidden_if_expr': '',
                'widget_mode_expr': '',
                'css_class': '',
                'css_class_expr': '',
                'javascript_expr': '',
            },
        },

        
    },
    'layout': {
        'style_prefix': 'layout_default_',
        'layout_create_method': '',
        'layout_edit_method': '',
        'layout_view_method': '',
        'flexible_widgets': (),
        'validate_values_expr': '',
        'ncols': 1,
        'rows': [
            [{'widget_id': 'map_id', 'ncols': 1},
            ],
            [{'widget_id': 'map_rendering', 'ncols': 1},
            ],
        ],
    },
}

layouts = {}
layouts['geolocation'] = cpsgeo_layout
layouts['map_document'] = map_document_layout

return layouts
