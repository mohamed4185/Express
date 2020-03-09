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

from odoo import api, fields, models


class PeriodicalReportWizard(models.TransientModel):
    _name = "periodical.report.purchase"

    """period = fields.Selection([
        ('today', 'Today'),
        ('last_week', 'Last Week'),
        ('last_month','Last Month')],
        'Period',
         default='today',
        help="Select the option for priting report for daily, "
             "weekly or monthly")
    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ('to approve','To Approve'),
        ('all', 'All')
        ], string='Status',  default='all')"""
    date_from = fields.Date(string='تاريخ البدء')
    date_to = fields.Date(string='تاريخ الانتهاء')
    product=fields.Many2one('product.product','المنتج')

    vendor=fields.Many2one('res.partner','المورد',domain="[('supplier','=',True)]")
    @api.multi
    def check_report(self):
        #period = self._fields['period'].get_values(self.env)
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_from': self.date_from,
                'date_to': self.date_to,
                'vendor':self.vendor.id,
                'product':self.product.id

              
            },
        }
        return self.env.ref('periodical_purchase_report.action_report_periodical_purchase').report_action(self, data=data)
