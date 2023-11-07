from odoo import api, models, fields

class ResUsers(models.Model):

    _inherit = "res.users"


    # Model name of the related properties
    # Field name in 'estate.property' that references the user
    # Restrict to only show properties where salesperson matches the user

    property_ids = fields.One2many("estate.property" , "salesman", string="Real Estate Properties" ,
                                                                domain = [('state', 'in' ,  ["new", "offer_received"])])
    
    
    show12 = fields.Many2many("res.partner", string = "Show fileds")
    # show1 = fields.Many2many("res.users", string = "Show fileds")