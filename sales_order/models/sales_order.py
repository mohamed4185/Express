from odoo import models, fields, api
from odoo.exceptions import ValidationError


class salesorder(models.Model):
    _inherit = 'sale.order'


