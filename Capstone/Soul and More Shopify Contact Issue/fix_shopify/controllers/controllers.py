# -*- coding: utf-8 -*-
# from odoo import http


# class InvoicableSaleLines(http.Controller):
#     @http.route('/invoicable_sale_lines/invoicable_sale_lines', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/invoicable_sale_lines/invoicable_sale_lines/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('invoicable_sale_lines.listing', {
#             'root': '/invoicable_sale_lines/invoicable_sale_lines',
#             'objects': http.request.env['invoicable_sale_lines.invoicable_sale_lines'].search([]),
#         })

#     @http.route('/invoicable_sale_lines/invoicable_sale_lines/objects/<model("invoicable_sale_lines.invoicable_sale_lines"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('invoicable_sale_lines.object', {
#             'object': obj
#         })

