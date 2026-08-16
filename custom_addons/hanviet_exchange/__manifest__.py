{
    'name': 'Han Viet KRW Exchange Analysis',
    'version': '1.0',
    'summary': 'KRW to VND exchange rate analysis with SMA and recommendation',
    'category': 'Finance',
    'author': 'Han Viet Supply',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/exchange_rate_views.xml',
        'views/exchange_rate_menus.xml',
    ],
    'application': True,
    'installable': True,
}
