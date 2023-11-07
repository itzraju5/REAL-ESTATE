from odoo import models, Command

class EstateProperty(models.Model):



    _inherit = 'estate.property'




#_______________________________________________________________________________________________________________________________________



    # def action_for_sold(self):
    #     print("**************** Inherited action_for_sold method works *********************")
        
    
    #     self.env["account.move"].create(
    #         {
    #             "partner_id": self.buyer.id,
    #             "move_type": "out_invoice",
                
            
    #             "invoice_line_ids": [
    #                     (
    #                         0,
    #                         0,
    #                         {
    #                             "name": self.name,
    #                             "quantity": 1.0,
    #                             "price_unit": self.selling_price * 6.0 / 100.0,
    #                         },
    #                     ),
    #                     (
    #                         0,
    #                         0,
    #                         {
    #                             "name": "Administrative fees",
    #                             "quantity": 1.0,
    #                             "price_unit": 100.0,
    #                         },
    #                     ),
    #                 ],
    #         }
    #     )

    #     return super().action_for_sold()


    def action_for_sold(self):
        print("**************** Inherited action_for_sold method works *********************")

        self.env['account.move'].create(
            {
                
                'partner_id' : self.buyer.id,
                'move_type' : 'out_invoice',
                'invoice_line_ids' : [
                   Command.create (

                        {
                            "name" :self.name,
                            "quantity" : 1,
                            "price_unit" : self.selling_price,
                        },
                    ),
                    Command.create(
                        {
                            "name" : "administrative fees",
                            "quantity" : 1,
                            "price_unit" : self.selling_price * 6.0 / 100.0,
                        },
                    )],
            }
        )
        return super().action_for_sold()

        