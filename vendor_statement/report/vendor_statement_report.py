from odoo import api, models
from dateutil.relativedelta import relativedelta
import datetime
import logging
import pytz
_logger = logging.getLogger(__name__)

class ReportProductSale(models.AbstractModel):
    _name = 'report.vendor_statement.vendor_statement_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        date_from = data['form']['date_from']
        date_to = data['form']['date_to']
        vendor=data['form']['vendor']
        analytical_account_id=data['form']['analytical_account_id']
         
        total_sale = 0.0
        period_value = ''
        domain=[('type','=','in_invoice')]
        if date_from:
            domain.append(('date_invoice', '>=', date_from))
        if date_to  :
            domain.append(('date_invoice', '<=', date_to))
        if vendor:
            domain.append(('partner_id', '=', vendor))

         
        list = []
        order_line=[]
        invoice_ids = self.env['account.invoice'].search(domain,order='date_invoice asc')
        old_timezone = pytz.timezone("UTC")
        new_timezone = pytz.timezone("Africa/Cairo") 
      
        for inv in invoice_ids:
                if inv.state!='draft':
                        date_so=''
                        
                        sale_order=self.env['purchase.order'].search([('name','=',inv.origin)])
                        if sale_order:
                            last_new_timezone = old_timezone.localize(sale_order.date_order).astimezone(new_timezone)
                            last_new_timezone=last_new_timezone.strftime('%Y-%m-%d')
                            date_so = last_new_timezone

                             

                        for line in inv.invoice_line_ids:
                                if  analytical_account_id:
                                     if line.account_analytic_id.id == analytical_account_id:
                                         list.append({
                                            'so_number':inv.origin,
                                            'date_so': date_so,
                                            'invoice_number':line.invoice_id.number,
                                            
                                            'product_id':line.product_id.name,
                                            'inv_name':line.invoice_id.name,
                                            'date_in':line.invoice_id.date_invoice,
                                            'partner' : line.invoice_id.partner_id.name,
                                            'quantity':line.quantity,
                                            'price_unit':line.price_unit,
                                            'total':line.price_total,
                                            'note_invoice':line.note_invoice

                                        })
                                else:
                                    list.append({
                                            'so_number':inv.origin,
                                            'date_so': date_so,
                                            'invoice_number':line.invoice_id.number,
                                            
                                            'product_id':line.product_id.name,
                                            'inv_name':line.invoice_id.name,
                                            'date_in':line.invoice_id.date_invoice,
                                            'partner' : line.invoice_id.partner_id.name,
                                            'quantity':line.quantity,
                                            'price_unit':line.price_unit,
                                            'total':line.price_total,
                                            'note_invoice':line.note_invoice

                                        })

        if len(list)!=0:

            return {
                'doc_ids': data['ids'],
                'doc_model': data['model'],
                'period' : period_value,
                'date_from': date_from,
                'date_to': date_to,
                'sale_orders' : list,
                'total_sale' : total_sale,
                'vendor_name':self.env['res.partner'].search([('id','=',vendor)]).name,
                'data_check':False,
                "analytical_account_id":self.env['account.analytic.account'].search([('id','=',analytical_account_id)]).name,
                "name_report":'كشــف حســـاب مــــــورد'
            }
        else:
            return {
                'doc_ids': data['ids'],
                'doc_model': data['model'],
                'period' : period_value,
                'date_from': date_from,
                'date_to': date_to,
                'sale_orders' : list,
                'total_sale' : total_sale,
                'vendor_name':self.env['res.partner'].search([('id','=',vendor)]).name,
                "analytical_account_id":self.env['account.analytic.account'].search([('id','=',analytical_account_id)]).name,
                'data_check':True,
                "analytical_account_id":self.env['account.analytic.account'].search([('id','=',analytical_account_id)]).name,
                "name_report":'كشــف حســـاب مــــــورد'
            }
