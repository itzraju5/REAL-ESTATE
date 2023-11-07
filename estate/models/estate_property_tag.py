from odoo import fields, models, api
from odoo.exceptions import ValidationError

class EstatePropertyTag(models.Model):

    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name"


    name = fields.Char(string="Name", required=True)
    # attribute = fields.Char(string="Attribute")
    color = fields.Integer(string = "Color")


#___________________________________________________________________________________________________________________________________


#   A property tag name must be unique

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)',
         'name Already exists'),

    ]

    # @api.constrains('name')
    # def check_name(self):
    #     for record in self:
    #         existing = self.env['estate.property.tag']. search([('name', '=', record.name)])
    #         if existing:
    #             raise ValidationError("Name %s Allready esists." % record.name)

    
    
   
