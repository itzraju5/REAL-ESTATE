from odoo import models, fields, api, Command
from dateutil.relativedelta import relativedelta


class EstatePropertyWizard(models.TransientModel):


    _name = 'estate.property.wizard'
    _description = 'Estate Property Wizard'




    # Define fields for the wizard
    price = fields.Float(string='Price', required=True)
    
    buyer = fields.Many2one('res.partner', string='Buyer Name', required=True)
    
    date_availability = fields.Date(
        'Available From', default=lambda self: fields.Date.today() + relativedelta(months=+3))
    
# _____________________________________________________________________________________________________________________________



    def action_make_offer(self):

        # Check if there are any selected properties, if not selected property return Default value means (Empty List []) 
        selected_properties = self.env.context.get('active_ids')
        # print("***************selected**************", self.env.context)
        print("***************selected**************", selected_properties)
        for rec in selected_properties:
            alloffer = self.env['estate.property.offer'].create({
                'property_id':rec,
                'price': self.price,
                'partner_id': self.buyer.id,
            })
            self.env['estate.property'].browse(rec).update({ 
                "state":'offer_received'
             }) 
        
            # print(alloffer)
        return alloffer
            
        # return {'type': 'ir.actions.act_window_close'}
      


            


    def cancel(self):
        return {'type': 'ir.actions.act_window_close'}


