
{
    'name': "Real estate account",
    'version': "1.0",
    'website': "www.odoo.com",
    'category': "Uncategorized",
    'application': True,
    'depends': ['estate', 'account'],
    'sequence': 0,
    'installable': True,
    "auto_install": True,
    'data': [
        'report/report_inherit.xml',
    ],
    

}
#  odoo ka default h base module pahle install hoga 