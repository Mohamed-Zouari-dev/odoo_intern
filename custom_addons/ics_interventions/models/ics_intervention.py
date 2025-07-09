from odoo import models, fields


# Not Necessary for the internship
# Not Necessary for the internship
# Not Necessary for the internship
# Not Necessary for the internship
# Not Necessary for the internship
# Not Necessary for the internship


class Intervention(models.Model):
    _name = 'ics.intervention'
    _description = 'Intervention'
    type_intervention = fields.Selection([('Réseau', 'Réseau'), ('Logiciel', 'Logiciel'), ('Formation', 'Formation')]),
    date_prevue = fields.Date('Date prévue / durée', help="Date de prevention")


    name = fields.Char('Nom de la intervention')
""" client = fields.Many2many(
     'res.partner',
     string='Client',
     domain="[('customer_rank', '>', 0)]"
 )"""
