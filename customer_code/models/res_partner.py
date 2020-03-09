# -*- coding: utf-8 -*-

from odoo import api, fields ,models
from odoo.exceptions import ValidationError 
import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit="res.partner"
     
    customer_code=fields.Char('Code',size=10)


     