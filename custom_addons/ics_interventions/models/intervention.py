from odoo import models, fields, api
from datetime import timedelta

class Intervention(models.Model):
    _name = 'ics.intervention'
    _description = 'Intervention Technique'



    name = fields.Char('Référence', required=True, default='Nouveau', copy=False)
    partner_id = fields.Many2one('res.partner', 'Client', required=True)
    type = fields.Selection([
        ('network', 'Réseau'),
        ('software', 'Logiciel'),
        ('training', 'Formation'),
        ],
        'Type', default='network', required=True)
    date_planned = fields.Datetime('Date prévue', required=True)
    duration = fields.Float('Durée (heures)')
    employee_id = fields.Many2one('hr.employee', 'Employé')
    state = fields.Selection([
        ('draft', 'A planifier'),
        ('in_progress', 'En cours'),
        ('done', 'Terminée')],
        'Statut', default='draft', tracking=True)

    def action_start(self):
        self.write({'state': 'in_progress'})

    def action_done(self):
        self.write({'state': 'done'})

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nouveau') == 'Nouveau':
            vals['name'] = self.env['ir.sequence'].next_by_code('ics.intervention') or 'Nouveau'
        return super().create(vals)

    # Ajouter dans models/intervention.py
    date_end = fields.Datetime('Date de fin')