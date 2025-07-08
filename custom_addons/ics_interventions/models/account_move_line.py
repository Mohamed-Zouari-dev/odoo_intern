from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    montant = fields.Float(string='Montant')


    code_ndp = fields.Many2one(string="Code NDP")
    total_montant = fields.Monetary(
        string="Montant Total Douane",
        compute='_compute_total_montant',
        store=True,
        currency_field='currency_id'
    )

    @api.depends('invoice_line_ids.montant')
    def _compute_total_montant(self):
        for move in self:
            move.total_montant = sum(line.montant for line in move.invoice_line_ids)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    code_ndp = fields.Char(
        string="Code NDP",
        related='product_id.code_ndp',
        store=True,
        readonly=False
    )
    tax = fields.Float(
        string="Taxe (%)",
        related='product_id.taux',
        store=True,
        readonly=False
    )
    montant = fields.Monetary(
        string="Montant (avec taxe)",
        compute='_compute_montant',
        store=True,
        currency_field='currency_id'
    )

    @api.depends('price_subtotal', 'tax')
    def _compute_montant(self):
        for line in self:
            line.montant = line.price_subtotal * (1 + line.tax / 100)
