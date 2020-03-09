# -*- coding: utf-8 -*-

###############################################################################
#
#    Periodical Sales Report
#
#    Copyright (C) 2019 Aminia Technology
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

{
    'name' : 'Total transactions report',
    'version' : '12.0.1',
    'summary': 'Executive report to monitor Total  transactions (debit & credit) for specific journal with type  cash',
    'sequence': 16,
    'category': 'Account',
    'author' : 'BBl',
    'description': """
Executive report to monitor Total  transactions (debit & credit) for specific journal with type  cash
    """,
    "license": "AGPL-3",
    'depends' : ['base_setup', 'sale_management','account','move_product_in_to_out'],
    'data': [
        'wizard/wiz_total_transactions_view.xml',
        'views/total_transactions_view.xml',
        'views/report_total_transactions.xml',
        'views/report_total_debit_transactions.xml',
        'views/report_total_credit_transactions.xml'
    ],
    
    'installable': True,
    'application': True,
    'auto_install': False,
}
