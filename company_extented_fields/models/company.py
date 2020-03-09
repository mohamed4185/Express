from odoo import models, fields, api
from odoo.exceptions import ValidationError


class invoices(models.Model):
    _inherit = 'res.company'
    fax = fields.Char('فاكس')
    company_info = fields.Text('بيانات إضافية')

