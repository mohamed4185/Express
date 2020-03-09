from odoo import api, models,fields
from dateutil.relativedelta import relativedelta
import datetime
import logging
_logger = logging.getLogger(__name__)

class report_list(models.Model):
    _name='list.rep.express'
    name=fields.Char('Name')
