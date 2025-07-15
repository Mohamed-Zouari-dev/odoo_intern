from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import timedelta


class Intervention(models.Model):
    _name = 'ics.intervention'
    _description = 'Intervention Technique'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ref = fields.Char('Référence', copy=False, readonly=True)
    partner_id = fields.Many2one('res.partner', 'Client', required=True, tracking=True)
    type_id = fields.Many2one('ics.intervention.type', 'Type', required=True, tracking=True)
    date_planned = fields.Datetime('Date prévue', required=True, tracking=True)
    duree = fields.Float('Durée (heures)', tracking=True)
    employee_id = fields.Many2one('hr.employee', 'Employé', tracking=True)
    state = fields.Selection([
        ('draft', 'A planifier'),
        ('in_progress', 'En cours'),
        ('done', 'Terminée')],
        string='Statut', default='draft', tracking=True)
    date_end = fields.Datetime('Date de fin', tracking=True)
    invoice_id = fields.Many2one('account.move', string='Facture associée', readonly=True, copy=False)
    description = fields.Text(string="Description de l'intervention", tracking=True)
    date_deadline = fields.Datetime('Date de fin prévue', compute='_compute_date_deadline', store=True)

    def action_create_invoice(self):
        self.ensure_one()

        if not self.type_id:
            raise UserError(_("Veuillez sélectionner un type d'intervention avant de créer une facture"))

        if not self.partner_id.property_account_receivable_id:
            raise UserError(_("Le client sélectionné n'a pas de compte comptable configuré"))

        product = self.type_id

        if not product:
            raise UserError(_("Le type d'intervention sélectionné n'a pas de produit lié."))

        invoice_line_vals = {
            'name': product.name,
            'product_id': product.product_id.id,
            'quantity': self.duree or 1.0,
            'price_unit' : 5

        }

        # create invoice
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'invoice_date': fields.Date.today(),
            'invoice_origin': self.ref,
            'invoice_line_ids': [(0, 0, invoice_line_vals)],
        })

        # link intervention to invoice
        self.invoice_id = invoice.id

        # return invoice form view
        return {
            'name': _('Facture Client'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'target': 'current',
            'views': [(self.env.ref('account.view_move_form').id, 'form')],
        }

    @api.depends('date_planned', 'duree')
    def _compute_date_deadline(self):
        for rec in self:
            if rec.date_planned and rec.duree:
                rec.date_deadline = rec.date_planned + timedelta(hours=rec.duree)
            else:
                rec.date_deadline = rec.date_planned

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

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('ref', 'Nouveau') == 'Nouveau':
                partner_name = self.env['res.partner'].browse(vals.get('partner_id')).name if vals.get(
                    'partner_id') else ''
                employee_name = self.env['hr.employee'].browse(vals.get('employee_id')).name if vals.get(
                    'employee_id') else ''
                date_str = fields.Datetime.from_string(vals['date_planned']).strftime('%d-%m-%Y') if vals.get(
                    'date_planned') else ''
                vals['ref'] = ' - '.join(filter(None, [partner_name, employee_name, date_str])) or 'Nouveau'
        return super().create(vals_list)

    def unlink(self):
        return super().unlink()

    def group_expand_state(self, states, domain, order):
        return self.env['ics.intervention'].search(domain, order=order)


class InterventionType(models.Model):
    _name = 'ics.intervention.type'
    _description = "Types d'intervention"
    _inherit = ['mail.thread']

    name = fields.Char('Type de service', required=True, tracking=True)

    product_id = fields.Many2one(
        'product.product',
        string="Produit/service lié",
        required=True,
        help="Produit/service utilisé pour la facturation"
    )