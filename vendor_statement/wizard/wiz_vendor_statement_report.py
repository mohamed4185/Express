
from odoo import api, fields, models


class PeriodicalReportProduct(models.TransientModel):
    _name = "vendor.statement"

     
    date_from = fields.Date(string='تاريخ البدء')
    date_to = fields.Date(string='تاريخ الانتهاء')
    vendor=fields.Many2one('res.partner','المورد',domain="[('supplier','=',True)]")
    analytical_account_id=fields.Many2one('account.analytic.account',string="الحساب التحليلي")
    @api.multi
    def check_report(self):
         
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_from': self.date_from,
                'date_to': self.date_to,
                'vendor':self.vendor.id,
                'analytical_account_id':self.analytical_account_id.id


            },
        }
        return self.env.ref('vendor_statement.action_report_vendor_statement').report_action(self, data=data)
