# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class DateReportWizard(models.TransientModel):
    _name = "workshop.date.report.wizard"
    _description = "Date Report"

    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)

    def print_report(self):
        workshop=self.env['workshop.workshop']
        domain=[
            ('reception_date','>=',self.start_date),
            ('reception_date','<=',self.end_date)
        ]
        workshopField = [
            'name',
            'description',
            'warranty',
            'reception_date',
            'labor_cost',
            'repair_parts_cost',
            'repair_total_cost',
        ]
        WorkshopRecords=workshop.search_read(domain,workshopField)
        data={
            'WorkshopRecords':WorkshopRecords,
            'start_date':self.start_date,
            'end_date':self.end_date,
        }
        return self.env.ref('workshop.report_DateReportExternalLayout').report_action(self, data=data)