from odoo import api, models
from dateutil.relativedelta import relativedelta
import datetime
import logging

_logger = logging.getLogger(__name__)


class ReportPartnerBalance(models.AbstractModel):
    _name = "report.partner_balance.partner_balance_report"

    @api.model
    def _get_report_values(self, docids, data=None):
        date_from = data["form"]["date_from"]
        date_to = data["form"]["date_to"]
        partner = data["form"]["partner"]
        vendor_mode = data["form"]["vendor_mode"]
        analytical_account_id=data["form"]["analytical_account_id"]
        report_name=""
        total_sale = 0.0
        period_value = ""
        domain = []
        if date_from:
            domain.append(("date", ">=", date_from))
        if date_to:
            domain.append(("date", "<=", date_to))
        if partner:
            domain.append(("partner_id", "=", partner))
        if analytical_account_id:
            domain.append(("analytic_account_id", "=", analytical_account_id))

        if vendor_mode==True:
           
            report_name="بيـــان بحسابـــــات الموردين الدائنون"
        if vendor_mode==False:
           
            report_name="بيـــان بحسابـــــات العملاء المدينــــون"



        list = []
        order_line = []
        account_move_line = self.env["account.move.line"].search(domain, order="date asc")
        partner_list=[]
        for rec in account_move_line:
               partner_list.append(rec.partner_id.id)
        partner_list=set(partner_list)
        _logger.info(partner_list)
        all_debit,all_creidt,count=0,0,0

        for part in partner_list:
            debit_partner=0
            credit_partner=0
            partner_name=''
            for line in account_move_line:
                if part==line.partner_id.id:
                    partner_name=line.partner_id.name
                    if vendor_mode==True and line.partner_id.supplier==True:
                        if (line.partner_id.property_account_payable_id==line.account_id or  line.partner_id.property_account_receivable_id==line.account_id)  :
                             debit_partner+=line.debit
                             credit_partner+=line.credit
                                   
                    elif vendor_mode==False and line.partner_id.customer==True:    
                        if (line.partner_id.property_account_payable_id==line.account_id or  line.partner_id.property_account_receivable_id==line.account_id):
                            debit_partner+=line.debit
                            credit_partner+=line.credit

            _logger.info(partner_name)
            _logger.info(debit_partner)
            _logger.info(credit_partner)
            user_name=self.env['res.partner'].search([('id','=',part)])
            if debit_partner-credit_partner!=0:
                if vendor_mode==False and user_name.customer==True :
                    count+=1
                    list.append(
                        {   "count":count,
                            "partner":partner_name,
                            "debit": debit_partner,
                            "credit": credit_partner,
                              
                              
                        }
                    )
                if vendor_mode==True and user_name.supplier==True:
                    count+=1
                    list.append(
                        {   "count":count,
                            "partner": partner_name,
                            "debit": debit_partner,
                            "credit": credit_partner,
                              
                              
                        }
                    )

        _logger.info('list')
        _logger.info(list)
        if len(list) != 0:
            return {
                "doc_ids": data["ids"],
                "doc_model": data["model"],
                "period": period_value,
                "date_from": date_from,
                "date_to": date_to,
                "list_move": list,
                "vendor_mode":vendor_mode,
                 
                "data_check": False,
                 "name_report":report_name
            }
        else:
            return {
                "doc_ids": data["ids"],
                "doc_model": data["model"],
                "period": period_value,
                "date_from": date_from,
                "date_to": date_to,
                "list_move": list,
                "vendor_mode":vendor_mode,
                 
                "data_check": True,
                "name_report":report_name
            }

