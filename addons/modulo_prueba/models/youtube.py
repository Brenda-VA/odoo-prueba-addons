#addons/modulo_prueba/models/youtube.py
from odoo import fields, models

class Youtube(models.Model):
    _name= 'modulo_prueba.youtube'
    _description='Youtube Test'

    name = fields.Char('Name', required= True)
    description = fields.Char('Description')
    move_id = fields.Many2one('account.move', string='Move')
