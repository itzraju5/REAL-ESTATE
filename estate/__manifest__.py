
{
    'name': "estate",
    'summary': "Property management",
    'description': "This module allows you to manage properties.",
    'version': "1.0",
    'author': "Your Name",
    'website': "www.odoo.com",
    'category': 'Real Estate/Brokerage',
    'application': True,
    'depends': ['mail', 'website'],
    'sequence': 0,
    'installable': True,
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'views/estate_property_views.xml', 
        'views/estate_property_offer_view.xml',
        'views/estate_property_type_views.xml' ,
        'views/estate_property_tag_views.xml' ,
        'views/res_users_views.xml',
        'views/template.xml', 
        
        "report/estate_reports_template.xml",
        "report/estate_report_views.xml",
        "wizard/estate_property_wizard_views.xml",

        'views/estate_menus.xml'
    ],
    
    'demo': [
        'data/estate_data.xml',
    ]
   
}
