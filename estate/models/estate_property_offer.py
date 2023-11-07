from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from datetime import date
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero



class EstatePropertyOffer(models.Model):

    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"





    name = fields.Char(string="Name")
    price = fields.Float(string="Offer Price")
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        string='State',
        copy=False,)

    partner_id = fields.Many2one(
        "res.partner", string="Partner id", required=True)

    property_id = fields.Many2one(
        "estate.property", string="Property id", required=True)
    
    
    # For stat button:
    property_type_id = fields.Many2one("estate.property.type", related="property_id.estate_property_type", string="Property Type")
    

    validity = fields.Integer(string='Validity Days', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline',
                                inverse='_inverse_date_deadline', readonly=False, store=True)

   

#______________________________________________________________________________________________________________________________________

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for ln in self:
            if ln.create_date:

                print("------->>>>>>>>>>", ln.create_date)

                print("---------------- if")
                ln.date_deadline = ln.create_date +  relativedelta(days=ln.validity)
            else:
                print("---------------- else")
                ln.date_deadline = date.today() + relativedelta(days=ln.validity)



    @api.depends('create_date', 'date_deadline')
    def _inverse_date_deadline(self):
        for record in self:
            print(record.date_deadline)
            print('**************', (record.date_deadline -
                  record.create_date.date()).days)
            record.validity = (record.date_deadline - record.create_date.date()).days



    #  An offer price must be strictly positive:

    _sql_constraints = [
        ("check_price", "CHECK(price > 0)",
         "Offer price must be strictly positive"),
    ]

    
    def action_accept_offer(self):
        # print('+++++++++++++++++++++++++++')
        for len1 in self:
            record1 = len1.mapped('property_id.offer.status')

            for record in len1:
                if 'accepted' in record1:
                    raise ValidationError('One Offer Allready acepted')

                else:
                    if  record.price >= self.property_id.expected_price * 0.9:
                        print (" 90 %")
                        record.status = 'accepted'
                        record.property_id.state = 'offer_accepted'
                        record.property_id.selling_price = record.price
                        record.property_id.buyer = record.partner_id
                    else:
                        raise models.ValidationError("Selling Price cannot be lower than 90% of the Expected Price.")
                        
    

    def action_refuse_offer(self):
        # print('-----------------------')
        self.status = 'refused'
        # print("working")
        self.property_id.selling_price = 0.00




    @api.model
    def create(self, vals):
        # Check if property_id and price are provide
        if 'property_id' in vals and 'price' in vals:
            # Find existing offers for the same property

            # existing_offers = self.env['estate.property.offer'].browse(vals['property_id'])
            existing_offers = self.env['estate.property.offer'].search([('property_id', '=', vals['property_id'])])

            if existing_offers:
                max_offer_amount = max(existing_offers.mapped('price'))
                if vals['price'] <= max_offer_amount:
                    raise ValidationError("The offer amount must be higher than %.2f" % max_offer_amount)
      
                else:   
                    print("***************Raju*************************")  
                    return super().create(vals)
    
            else:
            
                return super().create(vals)
