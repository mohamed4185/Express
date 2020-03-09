################################################################################ -*- coding: utf-8 -*-

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
import pytz
_logger = logging.getLogger(__name__)

class ReportProductSale(models.AbstractModel):
    _name = 'report.item_card.item_card_product'

    @api.model
    def _get_report_values(self, docids, data=None):
        date_from = data['form']['date_from']
        date_to = data['form']['date_to']
        pro=data['form']['product']
        analytical_account_id=data['form']['analytical_account_id']
         
        total_sale = 0.0
        period_value = ''
        domain=[]
        
         
        stock_pinking = []
        order_line=[]
        picking = self.env['stock.picking'].search(domain)
        ids=[]
        dates=[]
        if date_from:
           date_from=datetime.datetime.strptime(date_from, '%Y-%m-%d')
        if date_to:
            date_to=datetime.datetime.strptime(date_to, '%Y-%m-%d')

        old_timezone = pytz.timezone("UTC")
        new_timezone = pytz.timezone("Africa/Cairo") 
        if date_from or date_to:
            for rec in picking:
                 
                
                last_new_timezone = old_timezone.localize(rec.scheduled_date).astimezone(new_timezone)
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
                picking=self.env["stock.picking"].search([('id','in',ids)])
            else:
                picking=[]


            
         
        order_lines=self.env['sale.order.line'].search([])
        
        for rec in picking:
             
            if rec.state!='draft' and rec.picking_type_id.code=='outgoing':
                
                sale_order=self.env['sale.order.line'].search([('order_id','=',rec.sale_id.id),('product_id','=',rec.product_id.id)])
                _logger.info("SALE ORDER")
                _logger.info(sale_order)
                if sale_order:
                  for line in sale_order:
                    price=line.price_unit
                else:
                    price=rec.product_id.standard_price
                last_new_timezone = old_timezone.localize(rec.scheduled_date).astimezone(new_timezone)
                last_new_timezone=last_new_timezone.strftime('%Y-%m-%d')
                
                for order in rec.move_ids_without_package:
                  
                     
                    if   pro and  analytical_account_id:
                        if   pro==order.product_id.id  and order.analytic_account_id.id==analytical_account_id:
                            stock_pinking.append({
                                'name': order.name,
                                'product_id':order.product_id.name,
                                'analytical_account_id':  order.analytic_account_id.name,
                                'qty_out':order.quantity_done,
                                'quantity':order.product_uom_qty,
                                'total':price*order.product_uom_qty,
                                'price':price

                                 

                             
                            })
                    elif  pro:
                        if   pro==order.product_id.id:
                            stock_pinking.append({
                                'name': order.name,
                                'product_id':order.product_id.name,
                                'analytical_account_id':  order.analytic_account_id.name,
                                
                                'quantity':order.product_uom_qty,
                                'qty_out':order.quantity_done,
                                'total':price*order.product_uom_qty,
                                'price':price
                                 

                             
                            })
                    elif analytical_account_id:
                        if   analytical_account_id==order.analytic_account_id.id:
                            stock_pinking.append({
                                'name': order.name,
                                'product_id':order.product_id.name,
                                'analytical_account_id':  order.analytic_account_id.name,
                                
                                'quantity':order.product_uom_qty,
                                'qty_out':order.quantity_done,
                                'total':price*order.product_uom_qty,
                                'price':price
                                 

                             
                            })
                    else:
                            stock_pinking.append({
                                'name': order.name,
                                'product_id':order.product_id.name,
                                'analytical_account_id':  order.analytic_account_id.name,
                                
                                'quantity':order.product_uom_qty,
                                'qty_out':order.quantity_done,
                                'total':price*order.product_uom_qty,
                                'price':price

                                 

                             
                            })
        if date_from:
           date_from=date_from.strftime('%Y-%m-%d')
        if date_to:
           date_to=date_to.strftime('%Y-%m-%d')
        _logger.info("PICKING")
        _logger.info(stock_pinking)
        if len(stock_pinking)!=0:
            return {
                    'doc_ids': data['ids'],
                    'doc_model': data['model'],
                    'period' : period_value,
                    'date_from': date_from,
                    'date_to': date_to,
                    'stock_pinking' : stock_pinking,
                    
                    "product_name":self.env['product.product'].search([('id','=',pro)]).name,
                    'data_check':False,
                    'analytical_account_id':self.env['account.analytic.account'].search([('id','=',analytical_account_id)]).name,

                    'name_report':'تكلفه صرف اصناف علي معدات'

                }
        else:
            return {
                    'doc_ids': data['ids'],
                    'doc_model': data['model'],
                    'period' : period_value,
                    'date_from': date_from,
                    'date_to': date_to,
                    'stock_pinking' : stock_pinking,
                    
                    "product_name":self.env['product.product'].search([('id','=',pro)]).name,
                    'data_check':True,
                    'analytical_account_id':self.env['account.analytic.account'].search([('id','=',analytical_account_id)]).name,
                    'name_report':'تكلفه صرف اصناف علي معدات'
                }