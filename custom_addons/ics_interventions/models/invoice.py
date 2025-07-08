from odoo import models, fields, api


#Not Necessary for the internship
#Not Necessary for the internship
#Not Necessary for the internship
#Not Necessary for the internship
#Not Necessary for the internship
#Not Necessary for the internship



class AccountMove(models.Model):
    _inherit = 'account.move'


    tax = fields.Float(string='Taxe :',
                       readonly=True,)



    montant = fields.Float(
        string='Montant',
        store=True,
    )
    ics_client_id = fields.Many2one(
        'res.partner',
        string="Client",
        domain="[('customer_rank', '>', 0)]"
    )

    code_ndp = fields.Char(
        string="Code NDP Principal",
        compute='_compute_main_code_ndp',
        store=True
    )



    @api.depends('invoice_line_ids.product_id.code_ndp')
    def _compute_main_code_ndp(self):
        for move in self:
            if move.invoice_line_ids and move.invoice_line_ids[0].product_id:
                move.code_ndp = move.invoice_line_ids[0].product_id.code_ndp
            else:
                move.code_ndp = False