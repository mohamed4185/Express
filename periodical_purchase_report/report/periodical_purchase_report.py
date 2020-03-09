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
import pytz
from odoo import api, models
from dateutil.relativedelta import relativedelta
import datetime
import logging
from collections import OrderedDict

_logger = logging.getLogger(__name__)


class ReportPeriodicalSale(models.AbstractModel):
    _name = "report.periodical_purchase_report.report_periodical_purchase"

    @api.model
    def _get_report_values(self, docids, data=None):
        date_from = data["form"]["date_from"]
        date_to = data["form"]["date_to"]
        """period = data['form']['period']
        state = data['form']['state']"""
        total_sale = 0.0
        period_value = ""
        vendor = data["form"]["vendor"]
        product = data["form"]["product"]
        domain = []
        if vendor:
            domain.append(("partner_id", "=", vendor))

         

        orders = self.env["purchase.order"].search(domain, order="date_order asc")
        
        ids=[]
        dates=[]
        if date_from:
           date_from=datetime.datetime.strptime(date_from, '%Y-%m-%d')
        if date_to:
            date_to=datetime.datetime.strptime(date_to, '%Y-%m-%d')

        old_timezone = pytz.timezone("UTC")
        new_timezone = pytz.timezone("Africa/Cairo") 
        if date_from or date_to:
            for rec in orders:
                 
                
                last_new_timezone = old_timezone.localize(rec.date_order).astimezone(new_timezone)
                last_new_timezone=last_new_timezone.strftime('%Y-%m-%d')
                _logger.info("last_new_timezone")
                _logger.info(last_new_timezone)
                last_new_timezone=datetime.datetime.strptime(last_new_timezone, '%Y-%m-%d')
                if date_to and date_from:
                    if date_from<=last_new_timezone and date_to>=last_new_timezone:
                        ids.append(rec.id)
                elif date_from:
                    if date_from<=last_new_timezone:
                        ids.append(rec.id)
                elif date_to:
                    if date_to>=last_new_timezone :
                        ids.append(rec.id)

            if ids:
                orders=self.env["purchase.order"].search([('id','in',ids)],order="date_order asc")
            else:
                orders=[]
         
        sale_orders=[]
        for rec in orders:
            total_sale = 0
            if rec.state == "purchase" or rec.state == "done":
                last_new_timezone = old_timezone.localize(rec.date_order).astimezone(new_timezone)
                last_new_timezone=last_new_timezone.strftime('%Y-%m-%d')
                dates.append(last_new_timezone)
                for order in rec.order_line:
                    if product:
                        if product == order.product_id.id:
                            sale_orders.append(
                                {
                                    "name": order.name,
                                    "date_order": last_new_timezone,
                                    "partner": order.order_id.partner_id.name,
                                    "amount_total": order.price_subtotal,
                                    "order_id": order.order_id.name,
                                    "quantity": order.product_uom_qty,
                                    "price_unit": order.price_unit,
                                    "total": order.price_total,
                                    "code": order.order_id.partner_id.customer_code,
                                    "note_purchase": order.note_purchase,
                                }
                            )
                    else:
                        sale_orders.append(
                            {
                                "name": order.name,
                                "date_order": last_new_timezone,
                                "partner": order.order_id.partner_id.name,
                                "amount_total": order.price_subtotal,
                                "order_id": order.order_id.name,
                                "quantity": order.product_uom_qty,
                                "price_unit": order.price_unit,
                                "total": order.price_total,
                                "code": order.order_id.partner_id.customer_code,
                                "note_purchase": order.note_purchase,
                            }
                        )
                    total_sale += order.price_subtotal
        _logger.info("Purchase Order")
        _logger.info(sale_orders)
        _logger.info(list(OrderedDict.fromkeys(dates)))
        if date_from:
           date_from=date_from.strftime('%Y-%m-%d')
        if date_to:
           date_to=date_to.strftime('%Y-%m-%d')
        if len(sale_orders) != 0:
            return {
                "doc_ids": data["ids"],
                "doc_model": data["model"],
                "period": period_value,
                "date_from": date_from,
                "date_to": date_to,
                "sale_orders": sale_orders,
                "total_sale": total_sale,
                "vendor_name":self.env['res.partner'].search([('id','=',vendor)]).name,
                "product_name":self.env['product.product'].search([('id','=',product)]).name,
                "data_check": False,
                "dates":list(OrderedDict.fromkeys(dates)),
                'name_report':'بيان بالتوريدات اليومية'
            }
        else:
            return {
                "doc_ids": data["ids"],
                "doc_model": data["model"],
                "period": period_value,
                "date_from": date_from,
                "date_to": date_to,
                "sale_orders": sale_orders,
                "total_sale": total_sale,
                "vendor_name":self.env['res.partner'].search([('id','=',vendor)]).name,
                "product_name":self.env['product.product'].search([('id','=',product)]).name,
                "data_check": True,
                "dates":list(OrderedDict.fromkeys(dates)),
                'name_report':'بيان بالتوريدات اليومية'
            }
