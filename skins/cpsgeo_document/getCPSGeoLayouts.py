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
                'label': 'WGS84 Coordinates',
                'label_edit': 'WGS84 Coordinates',
                'description': '',
                'help':  'A string of location coordinates. A point location must be represented as a x (longitude east of Greenwich meridian) and y (latitude north of equator) pair in decimal degree units. For example: Paris: "2.40 48.7333", or Denver: "-105.0 39.75"',
                'is_i18n': False,
                'readonly_layout_modes': (),
                'hidden_layout_modes': ('edit', 'create'),
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

layouts = {}
layouts['geolocation'] = cpsgeo_layout

return layouts
