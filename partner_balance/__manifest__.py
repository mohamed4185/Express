
{
    'name' : 'Partner Balance',
    'version' : '12.0.1',
    'summary': 'Module all balance product .',
    'sequence': 16,
    'category': 'Account',
    'author' : 'BBl',
    'description': """
Custom Sales Report
=====================================
This module print daily, last week and last month sale report.
Also print report for particular duration.
    """,
    "license": "AGPL-3",
    'depends' : ['base_setup','account'],
    'data': [
        'wizard/wiz_partner_balance_view.xml',
        'views/partner_balance_view.xml',
        'views/report_partner_balance.xml'
    ],
    
    'installable': True,
    'application': True,
    'auto_install': False,
}
