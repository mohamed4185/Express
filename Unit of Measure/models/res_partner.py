# -*- coding: utf-8 -*-

from odoo import api, fields ,models
from odoo.exceptions import ValidationError 
import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit="uom.category"
     
    measure_type = fields.Selection([
        ('unit', 'Units'),
        ('weight', 'Weight'),
        ('time', 'Time'),
        ('length', 'Length'),
        ('volume', 'Volume'),
    ], string="نوع وحدة القياس")


     