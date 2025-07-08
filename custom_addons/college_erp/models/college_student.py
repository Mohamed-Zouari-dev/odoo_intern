from odoo import models, fields


class CollegeStudent(models.Model):
    _name = 'college.student'
    _description = "College Student"

    admission_number = fields.Char(string="Admission Number",required=True)
    admission_date = fields.Date(string="Admission Date",required=True)
    first_name = fields.Char(string="First Name",required=True)
    last_name = fields.Char(string="Last Name",required=True)
    email = fields.Char(string="Email",required=True)
