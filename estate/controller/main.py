from odoo import http
from odoo.http import request



class Estate(http.Controller):

    @http.route('/estate/estate/', website=True, auth='public')
    def estate(self, **kw):
        return "Hello , World!"



    @http.route('/estate1/estate1/', website=True, auth='public')
    def estate(self, **kw):


        return http.request.render('estate.index',{})