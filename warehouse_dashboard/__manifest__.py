# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "warehouse dashboard",
    'version': "1.0",
    'category': "Stock",
    'depends': ['stock_enterprise',],
    'data': [
        'report/stock_report_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
}
