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
    _name = "product.move"

     
    date_from = fields.Date(string='تاريخ البدء')
    date_to = fields.Date(string='تاريخ الانتهاء')
    product=fields.Many2one('product.product','المنتج')
    analytical_account_id=fields.Many2one('account.analytic.account',string="الحساب التحليلي")
    @api.multi
    def check_report(self):
         
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_from': self.date_from,
                'date_to': self.date_to,
                'product':self.product.id,
                'analytical_account_id':self.analytical_account_id.id


            },
        }
        return self.env.ref('product_move.action_report_product_move').report_action(self, data=data)
