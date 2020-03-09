from odoo import api, models
from dateutil.relativedelta import relativedelta
import datetime
import logging

_logger = logging.getLogger(__name__)


class ReportProductSale(models.AbstractModel):
    _name = "report.total_transactions.total_debit_transactions_report"
    @api.model
    def _get_report_values(self, docids, data=None):
        date_from = data['form']['date_from']
        date_to = data['form']['date_to']
        journal_id = data['form']['journal_id']
        account_id = data['form']['account_id']
        doamin_cheq=[('move_id.state','=','posted')]
        if date_from:
            doamin_cheq.append(("date", ">=", date_from))
        if date_to:
            doamin_cheq.append(("date", "<=", date_to))
        if journal_id:
            doamin_cheq.append(("journal_id","=",journal_id))
        if account_id:
            doamin_cheq.append(("account_id","=",account_id))
        
        debit_list = []
        credit_list = []
        
        move_list = self.env['account.move.line'].search(doamin_cheq, order='date asc')
        user_log=self.env['res.users'].search([('id','=',self.env.uid)])
        type_jfr=''
        if user_log.lang=='en_US':
            type_jfr='cash'
        elif user_log.lang=='en_AA' or user_log.lang=='ar_SY':
            type_jfr='نقدي'

            
        for line in move_list:
            if line.journal_id.type=='cash':
                ref=''

                if line.payment_id.communication:
                    ref=line.payment_id.communication
                elif line.move_id.ref:
                    ref=line.move_id.ref
                else:
                    ref=line.name


                if line.account_id.id==line.journal_id.default_debit_account_id.id or line.account_id==line.journal_id.default_credit_account_id.id:
                    if line.debit>0:
                            debit_list.append({
                                'date': line.date,
                                'rerference':ref,
                                'Amount':line.debit
                            })
                    if line.credit>0:
                            credit_list.append({
                                'date': line.date,
                                'rerference':ref,
                                'Amount':line.credit
                            })
                    

                    
        if len(debit_list)!=0 or len(credit_list) !=0:

            return {
                'doc_ids': data['ids'],
                'doc_model': data['model'],
                'date_from': date_from,
                'date_to': date_to,
                'data_check':False,
                'debit_list':debit_list,
                'credit_list':credit_list,
                'journal_id':self.env['account.journal'].search([('id','=',journal_id)]).name,
                "name_report":'كشــف وارد وصادر خزينه'
            }
        else:
            return {
                'doc_ids': data['ids'],
                'doc_model': data['model'],
                'date_from': date_from,
                'date_to': date_to,
                'data_check':True,
                'debit_list':debit_list,
                'credit_list':credit_list,
                'journal_id':self.env['account.journal'].search([('id','=',journal_id)]).name,
                "name_report":'كشــف وارد وصادر خزينه '
            }