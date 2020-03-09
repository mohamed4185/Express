
import pytz
from odoo import api, models
from dateutil.relativedelta import relativedelta
import datetime
import logging
_logger = logging.getLogger(__name__)

class ReportProductPurchase(models.AbstractModel):
    _name = 'report.total_purchases_product.total_size_purchases_bar_product'

    @api.model
    def _get_report_values(self, docids, data=None):
        date_from = data['form']['date_from']
        date_to = data['form']['date_to']
        pro=data['form']['product']
        vendor=data['form']['vendor']
        analytical_account_id=data['form']['analytical_account_id']

        total_sale = 0.0
        period_value = ''
        domain=[]
        
        if vendor:
            domain.append(('partner_id','=',vendor))
         
        sale_orders = []
        order_line=[]
        orders = self.env['purchase.order'].search(domain,order="date_order desc")
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
                orders=self.env["purchase.order"].search([('id','in',ids)],order="date_order desc")
            else:
                orders=[]
         
        
        _logger.info('PRODUCT')
        _logger.info(type(pro))
        
        for rec in orders:
            total_sale=0
            count_invoice=0
            s_order_line_list=[]
            if rec.state=='purchase' or rec.state == "done":
                count_invoice=len(rec.invoice_ids)
                for order in rec.order_line:
                        _logger.info(type(order.product_id.id))
                        _logger.info(pro)
                        count_invoice=0
                        count_sale=0
                        s_order_line=self.env['purchase.order.line'].search([('order_id','=',rec.id),('product_id','=',order.product_id.id)])
                        
                        for lst in s_order_line:
                             

                            if lst.product_id.id not in s_order_line_list:
                                count_sale=1
                                count_invoice=len(rec.invoice_ids)
                               
                                s_order_line_list.append(lst.product_id.id)
                        if pro and analytical_account_id: 
                            if pro==order.product_id.id and analytical_account_id==order.account_analytic_id.id:
                                sale_orders.append({
                                    'name': order.name,
                                    'product_id':order.product_id.name,
                                     
                                    'partner' : order.partner_id.name, 
                                    'quantity':order.product_qty,
                                    'price_unit':order.price_unit,
                                    'count_invoice':count_invoice,
                                    'total':order.price_total,
                                    'pro_id':order.product_id,
                                    'count_sale':count_sale,
                                    'category':order.product_id.categ_id

                                 
                                })
                        elif pro: 
                            if pro==order.product_id.id:
                                sale_orders.append({
                                    'name': order.name,
                                    'product_id':order.product_id.name,
                                     
                                    'partner' : order.partner_id.name, 
                                    'quantity':order.product_qty,
                                    'price_unit':order.price_unit,
                                    'count_invoice':count_invoice,
                                    'total':order.price_total,
                                    'pro_id':order.product_id,
                                    'count_sale':count_sale,
                                    'category':order.product_id.categ_id

                                 
                                })
                        elif analytical_account_id: 
                            if analytical_account_id==order.account_analytic_id.id:
                                sale_orders.append({
                                    'name': order.name,
                                    'product_id':order.product_id.name,
                                     
                                    'partner' : order.partner_id.name, 
                                    'quantity':order.product_qty,
                                    'price_unit':order.price_unit,
                                    'count_sale':count_sale,
                                    'count_invoice':count_invoice,
                                    'total':order.price_total,
                                    'pro_id':order.product_id,
                                    'category':order.product_id.categ_id

                                 
                                })
                        else:
                            sale_orders.append({
                                    'name': order.name,
                                    'product_id':order.product_id.name,
                                     
                                    'partner' : order.partner_id.name,
                                    'quantity':order.product_qty,
                                    'price_unit':order.price_unit,
                                    'count_invoice':count_invoice,
                                    'count_sale':count_sale,
                                    'total':order.price_total,
                                    'pro_id':order.product_id,
                                    'category':order.product_id.categ_id})



        if date_from:
           date_from=date_from.strftime('%Y-%m-%d')
        if date_to:
           date_to=date_to.strftime('%Y-%m-%d')
        if len(sale_orders)!=0:
                return {
                    'doc_ids': data['ids'],
                    'doc_model': data['model'],
                    'period' : period_value,
                    'date_from': date_from,
                    'date_to': date_to,
                    'sale_orders' : sale_orders,
                    'total_sale' : total_sale,
                    'vendor_name':self.env['res.partner'].search([('id','=',vendor)]).name,
                    'product_name':self.env['product.product'].search([('id','=',pro)]).name,
                    'data_check':False,
                    'analytical_account_id':self.env['account.analytic.account'].search([('id','=',analytical_account_id)]).name,
                    'name_report':'اجمالي حجم المشتريات خلال فتره علي مستوي المصانع'
                }
        else:
            return {
                    'doc_ids': data['ids'],
                    'doc_model': data['model'],
                    'period' : period_value,
                    'date_from': date_from,
                    'date_to': date_to,
                    'sale_orders' : sale_orders,
                    'total_sale' : total_sale,
                    'vendor_name':self.env['res.partner'].search([('id','=',vendor)]).name,
                    'product_name':self.env['product.product'].search([('id','=',pro)]).name,
                    'data_check':True,
                    'analytical_account_id':self.env['account.analytic.account'].search([('id','=',analytical_account_id)]).name,
                    'name_report':'اجمالي حجم المشتريات خلال فتره علي مستوي المصانع'

                }
