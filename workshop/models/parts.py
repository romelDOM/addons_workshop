# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class WorkshopParts(models.Model):
    _name = "workshop.parts"
    _description = "Inventory of Parts"

    name = fields.Char(string='Name', required=True)
    stock = fields.Integer(string='Stock', required=True)
    price = fields.Float(string='Price', required=True)