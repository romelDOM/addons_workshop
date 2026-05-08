# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class workshop(models.Model):
    _name = 'workshop.workshop'
    _description = 'Workshop'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description', required=True)
    warranty = fields.Boolean(string='Warranty', required=True, default=False)
    reception_date = fields.Date(string='Reception Date', required=True, default=fields.Date.today())
    completion_date = fields.Date(string='Completion Date')
    labor_cost = fields.Float(string='Labor Cost', required=True)
    repair_parts_cost = fields.Float(string='Parts Cost', required=True, compute='_depends_set_repair_parts_cost')
    repair_total_cost = fields.Float(string='Total Cost', required=True, compute='_depends_set_repair_total_cost')
    parts_ids = fields.Many2many(
        "workshop.parts",
        string="Parts",
        required=True
    )
    status = fields.Selection(
        [
            ('received', 'Received'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
        ],
        required=True,
        default='received'
    )

    @api.depends('labor_cost', 'repair_parts_cost')
    def _depends_set_repair_total_cost(self):
        for record in self:
            record.repair_total_cost=record.labor_cost+record.repair_parts_cost
    
    @api.depends('parts_ids')
    def _depends_set_repair_parts_cost(self):
        for record in self:
            record.repair_parts_cost=0
            for part in record.parts_ids:
                record.repair_parts_cost+=part.price

    @api.onchange('warranty')
    def _onchange_warranty(self):
        for record in self:
            if record.warranty:
                record.repair_parts_cost=0
                record.labor_cost=0

    @api.constrains('labor_cost', 'repair_parts_cost')
    def _constrains_negative_values(self):
        for record in self:
            if record.labor_cost < 0:
                raise ValidationError('Labor cost cannot be negative')
            if record.repair_parts_cost < 0:
                raise ValidationError('Parts cost cannot be negative')