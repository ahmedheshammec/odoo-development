# -*- coding: utf-8 -*-
{
    'name': "my_module",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "Ahmed Hesham",
    'website': "https://wa.me/qr/JQIDUJQE2B7OM1",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'portal', 'mail', 'utm', 'report_xlsx'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/level.xml',
        'data/data.xml',
        'views/my_module_settings.xml',
        'views/templates.xml',
        'reports/report.xml',
        'wizard/report_student_wizard.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'license': 'LGPL-3',
}

# This is a Commit to delete later