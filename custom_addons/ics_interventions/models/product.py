from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    fournisseur = fields.Many2many(
        'res.partner',
        string='Fournisseur',
        domain="[('supplier_rank', '>', 0)]",
        help="Fournisseur principal de ce produit"
    )

    fournisseur_list = fields.Char(
        string='Fournisseurs',
        compute='_compute_fournisseur_list',
        store=True,
        compute_sudo=True,
        readonly=True
    )

    montant = fields.Monetary(
        string='Prix unitaire',
        related='product_tmpl_id.montant',
        store=True,
        readonly=False
    )

    code_ndp = fields.Char(
        string='Code NDP',
        related='product_tmpl_id.code_ndp',
        store=True,
        readonly=False
    )

    taux = fields.Float(
        string='Taux de Taxe',
        related='product_tmpl_id.taux',
        store=True,
        readonly=False
    )

    @api.depends('fournisseur', 'product_tmpl_id.fournisseur')
    def _compute_fournisseur_list(self):
        for product in self:
            # Get suppliers from variant or template
            suppliers = product.fournisseur or product.product_tmpl_id.fournisseur
            product.fournisseur_list = ', '.join(suppliers.mapped('name')) if suppliers else ''


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    fournisseur = fields.Many2many(
        'res.partner',
        string='Fournisseur',
        domain="[('supplier_rank', '>', 0)]",
        help="Fournisseur principal de ce produit"
    )

    fournisseur_list = fields.Char(
        string='Fournisseurs',
        compute='_compute_fournisseur_list',
        store=True,
        compute_sudo=True,
        readonly=True
    )

    montant = fields.Monetary(string='Prix unitaire')
    code_ndp = fields.Char(string='Code NDP')
    taux = fields.Float(string='Taux de Taxe')

    @api.depends('fournisseur')
    def _compute_fournisseur_list(self):
        for template in self:
            template.fournisseur_list = ', '.join(template.fournisseur.mapped('name')) if template.fournisseur else ''