# -*- coding: utf-8 -*-

from odoo import api, fields ,models
from odoo.exceptions import ValidationError 
import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit="sale.order"

    creation_date=fields.Date('تاريخ الانشاء')