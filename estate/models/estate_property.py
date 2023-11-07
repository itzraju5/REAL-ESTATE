from odoo import api, models, fields
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero
import random


class EstateProperty(models.Model):

# ---------------------------------------- Private Attributes ---------------------------------
    _name = 'estate.property'
    _description = "Our own business"
    _order = "id desc"

    _inherit = ['mail.thread', 'mail.activity.mixin']


#  A property expected price must be strictly positive:
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'expected price must be strictly positive'),

        ("check_selling_price", "CHECK(selling_price >= 0)",
         "Selling price must be non-negative"),

    ]


# --------------------------------------- Fields Declaration ----------------------------------


    name = fields.Char('Name', required=True, tracking=True)
    postcode = fields.Char('Postcode',
                           help='The postel code associated with the property')

    date_availability = fields.Date(
        'Available From', default=lambda self: fields.Date.today() + relativedelta(months=+3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling price', default=0.0, copy=False, readonly=True)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area(sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area(sqm)')

    description = fields.Char(string='description')

    garden_orientation = fields.Selection(selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
                                          string='Garden Orientation')

    last_seen = fields.Datetime(
        "Last Seen", default=lambda self: fields.Datetime.now())

    active = fields.Boolean(default=True)

    state = fields.Selection(
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'),
                   ('sold', 'Sold'), ('canceled', 'Canceled')],
        string='State',
        required=True,
        copy=False,
        default='new')

    estate_property_type = fields.Many2one( "estate.property.type", string="Property Type")

    estate_property_tag = fields.Many2many("estate.property.tag", string="Property Tag")

    buyer = fields.Many2one("res.partner", string="Buyer")
#     salesman = fields.Char(default=lambda self:self.env.user, string="Seller")

#     selling_person = fields.Many2one("res.users" ,default=lambda self:self.env.user, string="Selling person")

    salesman = fields.Many2one("res.users", string="Salesman" , default = lambda self:self.env.user)

#   offer_id
    offer = fields.One2many("estate.property.offer", "property_id", string="Offers")

    # total_area      =   fields.Float('Total Area(sqm)')
    total_area = fields.Float(
        string='Total Area (sq ft)', compute='_compute_total_area')

    # best_offer = fields.Float('Best Offer')
    best_offer = fields.Float(string='Best Offer', compute='_compute_best_offer')
    

    progress = fields.Integer(string = "Progress", compute='_compute_progress')
   



# ---------------------------------------- Compute methods ------------------------------------


    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for len in self:
            len.total_area = len.living_area + len.garden_area

    @api.depends('offer.price')
    def _compute_best_offer(self):
        for i in self:
            if i.offer:
                if i.state == 'new':
                    i.state = 'offer_received'
            else:
                i.state = 'new'

        # for len1 in self:
        #     len1.best_offer = max(len1.offer.mapped('price'), default=0)
        max = 0
        # print("------------------------", self.env['estate.property.offer'].search([('id', '=', 5)]))
        # print("------------------------", self.offer.read())
        values = self.mapped("offer.price")
        # print("--------------", max(values))
        for i in values:
            if i > max:
                max = i
        self.best_offer = max




 # ----------------------------------- Onchanges ---------------------------------------------

    @api.onchange('garden')
    def _onchange_garden(self):
        if (self.garden):
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False


# ---------------------------------------- Action Methods -------------------------------------

    def action_for_cancel(self):
        # breakpoint()
        if self.state == "sold":
            raise ValidationError('Sold Property cannot be cancelled')
        else:
            self.state = "canceled"

    def action_for_sold(self):
        if self.state == "sold":
            raise ValidationError('Property Allready sold')
        else:
            self.state = "sold"



#--------------------------------------------------CRUD METHODS------------------------------------------------------------

    @api.model_create_multi
    def create(self, vals):
        res = super(EstateProperty, self).create(vals)
        print("Hello Create-----------------------")

        print("self-------------------", self)      # current object
        print("res--------------------", res)       # current object & their id
        print("vals-------------------", vals)      # fields value

        
        for rec in vals:
            name = rec.get('name')
            postcode = rec.get('postcode')
            print("Name:", name)
            print("Postcode:", postcode)

        return res

    

    def write(self, vals):
        res = super().write(vals)
        print("Hello Update------------------------")

        print("self-------------------", self)      # current object & id
        print("res--------------------", res)       # True --- because the creation of the estate.property record was successful.
        print("vals-------------------", vals)      # fields value that are update

        print("--------------------", self.name)
        return res


# It should not be possible to delete a property which is not new or canceled.

    @api.ondelete(at_uninstall=False)
    def unlink_property(self):
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise ValidationError("You can't delete a property which is not new or canceled")
        # super().unlink()
                
    

    @api.depends('state')
    def _compute_progress(self):
        for rec in self:
            if rec.state == 'new':
                rec.progress = random.randrange(1,24)
            elif rec.state == 'offer_received':
                rec.progress = random.randrange(25,49)
            elif rec.state == 'offer_accepted':
                rec.progress = random.randrange(50,75)
            elif rec.state == 'sold':
                rec.progress = 100
            elif rec.state == 'canceled':
                rec.progress = 0





    def action_open_offer_wizard(self):
        print("++++++++++++++++++++++++++++")
        return {
            'name': 'Add an Offer to a Property',
            'type': 'ir.actions.act_window',
            'res_model': 'estate.property.wizard',
            'view_mode': 'form',
            # to get the reference to the view with the specified XML ID. 
            'view_id': self.env.ref('estate.view_estate_property_wizard_form').id,
            'target': 'new',
        }
    
    

