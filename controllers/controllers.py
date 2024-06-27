# -*- coding: utf-8 -*-
# from odoo import http


# class HotelGestion(http.Controller):
#     @http.route('/hotel_gestion/hotel_gestion', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hotel_gestion/hotel_gestion/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hotel_gestion.listing', {
#             'root': '/hotel_gestion/hotel_gestion',
#             'objects': http.request.env['hotel_gestion.hotel_gestion'].search([]),
#         })

#     @http.route('/hotel_gestion/hotel_gestion/objects/<model("hotel_gestion.hotel_gestion"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hotel_gestion.object', {
#             'object': obj
#         })
