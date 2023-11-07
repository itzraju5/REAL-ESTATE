from odoo import fields, models
from odoo.exceptions import ValidationError
from odoo import api

class EstatePropertyType(models.Model):

    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "name"


    
    name = fields.Char("Name",required=True)
    
    # attribute = fields.Char("Attribute", required=True)

    sequence = fields.Integer(string = "Sequence")
    
    offer_list = fields.One2many("estate.property", "estate_property_type", string="")

    offer_count = fields.Integer(string="Offers Count", compute="_compute_offer_count")

    


#___________________________________________________________________________________________________________________________________________________



#   A property type name must be unique

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)',
         'name Already exists'),

    ]


#    Compute offer count

    @api.depends('offer_list.offer')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_list.offer)


    # def action_view_offers(self):
    #     return {
    #         'name': 'Offers',
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'estate.property.offer',
    #         'domain': [('property_type_id', '=', self.id)],
    #         'view_mode': 'tree,form',
    #     }
    
