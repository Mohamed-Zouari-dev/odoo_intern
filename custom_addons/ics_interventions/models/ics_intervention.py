from odoo import models, fields, api
from datetime import timedelta

class Intervention(models.Model):
    _name = 'ics.intervention'
    _description = 'Intervention Technique'

    ref = fields.Char('Référence', copy=False)

    partner_id = fields.Many2one('res.partner', 'Client', required=True)
    type_id = fields.Many2one('ics.intervention.type', 'Type', required=True)
    date_planned = fields.Datetime('Date prévue', required=True)
    duration = fields.Float('Durée (heures)')
    employee_id = fields.Many2one('hr.employee', 'Employé')
    state = fields.Selection([
        ('draft', 'A planifier'),
        ('in_progress', 'En cours'),
        ('done', 'Terminée')],
        string='Statut', default='draft', tracking=True)
    date_end = fields.Datetime('Date de fin')

    def action_start(self):
        self.write({'state': 'in_progress'})

    def action_done(self):
        self.write({'state': 'done'})

    date_deadline = fields.Datetime('Date de fin prévue', compute='_compute_date_deadline', store=True)

    @api.depends('date_planned', 'duration')
    def _compute_date_deadline(self):
        for rec in self:
            if rec.date_planned and rec.duration:
                rec.date_deadline = rec.date_planned + timedelta(hours=rec.duration)
            else:
                rec.date_deadline = rec.date_planned
    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        if 'type_id' in fields_list:
            default_type = self.env['ics.intervention.type'].search([('name', '=', 'Réseau')], limit=1)
            if default_type:
                defaults['type_id'] = default_type.id
        return defaults

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('ref', 'Nouveau') == 'Nouveau':
                partner_name = ''
                employee_name = ''
                date_str = ''

                if 'partner_id' in vals:
                    partner = self.env['res.partner'].browse(vals['partner_id'])
                    partner_name = partner.name or ''

                if 'employee_id' in vals:
                    employee = self.env['hr.employee'].browse(vals['employee_id'])
                    employee_name = employee.name or ''

                if 'date_planned' in vals:
                    try:
                        dt = fields.Datetime.from_string(vals['date_planned'])
                        date_str = dt.strftime('%d-%m-%Y')
                    except Exception:
                        date_str = ''

                ref_parts = [partner_name, employee_name, date_str]
                vals['ref'] = ' - '.join(p for p in ref_parts if p) or 'Nouveau'

        return super().create(vals_list)
    def unlink(self):

        return super().unlink()

    def group_expand_state(self, states, domain, order):
        selection = dict(self._fields['state'].selection)
        return self.env['ics.intervention'].browse([]).with_context(
            _group_expand_states=list(selection.keys())
        )

    description = fields.Text(string="Description de l'intervention")


class InterventionType(models.Model):
    _name = 'ics.intervention.type'
    _description = "Types d'intervention"

    name = fields.Char('Type', required=True)
    description = fields.Text('Description')
