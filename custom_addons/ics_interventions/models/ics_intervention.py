from odoo import models, fields, api
from odoo.exceptions import UserError

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

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        if 'type_id' in fields_list:
            default_type = self.env['ics.intervention.type'].search([('name', '=', 'Réseau')], limit=1)
            if default_type:
                defaults['type_id'] = default_type.id
        return defaults

    @api.model
    def create(self, vals):
        if vals.get('ref', 'Nouveau') == 'Nouveau':
            partner_name = ''
            employee_name = ''
            date_str = ''

            # Get partner name
            if 'partner_id' in vals and vals['partner_id']:
                partner = self.env['res.partner'].browse(vals['partner_id'])
                partner_name = partner.name or ''

            # Get employee name
            if 'employee_id' in vals and vals['employee_id']:
                employee = self.env['hr.employee'].browse(vals['employee_id'])
                employee_name = employee.name or ''

            # Format date planned
            if 'date_planned' in vals and vals['date_planned']:
                try:
                    dt = fields.Datetime.from_string(vals['date_planned'])
                    date_str = dt.strftime('%Y-%m-%d')
                except Exception:
                    date_str = ''

            # Compose ref string
            ref_parts = [partner_name, employee_name, date_str]
            ref_parts = [p for p in ref_parts if p]  # remove empty parts
            ref = ' - '.join(ref_parts)

            # If empty ref fallback to default 'Nouveau'
            vals['ref'] = ref or 'Nouveau'

        return super().create(vals)

    def unlink(self):
        for record in self:
            if record.state != 'done':
                raise UserError("Vous ne pouvez supprimer que les interventions terminées.")
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
