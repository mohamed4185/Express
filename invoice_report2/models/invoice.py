from odoo import models,fields, api
from odoo.exceptions import ValidationError

class invoices(models.Model):
    _inherit='account.invoice'
      

