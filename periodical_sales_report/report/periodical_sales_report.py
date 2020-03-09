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

from odoo import api, models
from dateutil.relativedelta import relativedelta
import datetime
import logging
import datetime
import pytz # new import
from collections import OrderedDict

_logger = logging.getLogger(__name__)


class ReportPeriodicalSale(models.AbstractModel):
    _name = "report.periodical_sales_report.report_periodical_sales"

    @api.model
    def _get_report_values(self, docids, data=None):
        date_from = data["form"]["date_from"]
        date_to = data["form"]["date_to"]
        customer = data["form"]["customer"]
        product = data["form"]["product"]
        analytical_account_id=data["form"]["analytical_account_id"]

        total_sale = 0.0
        period_value = ""
        domain = []
        if customer:
            domain.append(("partner_id", "=", customer))

        orders = self.env["sale.order"].search(domain, order="date_order asc")
        

        sale_orders = []
        order_line = []
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
                last_new_timezone=datetime.datetime.strptime(last_new_timezone, '%Y-%m-%d')
                _logger.info("last_new_timezone")
                _logger.info(last_new_timezone)
                _logger.info(date_from)
                _logger.info(type(last_new_timezone))
                _logger.info(type(date_from))
                
               
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
               orders=self.env["sale.order"].search([('id','in',ids)],order="date_order asc")
            else:
                orders=[]
        _logger.info("IDDDDDD") 
        _logger.info(ids)
        for rec in orders:
            total_sale = 0
            if rec.state == "sale" or rec.state == "done":
                last_new_timezone = old_timezone.localize(rec.date_order).astimezone(new_timezone)
                last_new_timezone=last_new_timezone.strftime('%Y-%m-%d')
                dates.append(last_new_timezone)
                for order in rec.order_line:
                    if product and analytical_account_id:
                        if order.product_id.id == product and order.analytical_account_id.id == analytical_account_id:
                            
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
                                    "note_sale": order.note_sale,
                                    
                                }
                            )

                    elif analytical_account_id:
                        if order.analytical_account_id.id == analytical_account_id:
                            
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
                                    "note_sale": order.note_sale,
                                    
                                }
                            )

                    elif product:
                        if order.product_id.id == product:
                            
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
                                    "note_sale": order.note_sale,
                                    
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
                                "note_sale": order.note_sale,
                            }
                        )
                    total_sale += order.price_subtotal
        for rec in sale_orders:
            _logger.info(rec['date_order'])
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
                "customer_name":self.env['res.partner'].search([('id','=',customer)]).name,
                "product_name":self.env['product.product'].search([('id','=',product)]).name,
                "st":self.env["sale.order"].search([('state','=','done')]),
                "data_check": False,
                "analytical_account_id":self.env['account.analytic.account'].search([('id','=',analytical_account_id)]).name,
                "dates":list(OrderedDict.fromkeys(dates)),
                'name_report':'بيان بالمبيعات اليوميه'
                
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
                "customer_name":self.env['res.partner'].search([('id','=',customer)]).name,
                "product_name":self.env['product.product'].search([('id','=',product)]).name,
                "st":self.env["sale.order"].search([('state','=','done')]),
                "data_check": True,
                "analytical_account_id":self.env['account.analytic.account'].search([('id','=',analytical_account_id)]).name,
                "dates":list(OrderedDict.fromkeys(dates)),
                'name_report':'بيان بالمبيعات اليوميه'
            }

