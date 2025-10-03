from odoo import http
from odoo.http import request
import json

class EstatePropertyController(http.Controller):

    @http.route('/properties/unsold_properties', auth='public', methods=['GET'])
    def get_unsold_properties(self):
        properties = request.env['estate.property'].sudo().search([('state', '!=', 'sold')])

        properties_data = []
        for prop in properties:
            properties_data.append({"name": prop.name,
                                    "description": prop.description,
                                    "salesman_id": prop.salesman_id.name,
                                    "postcode": prop.postcode,
                                    "selling_price": prop.selling_price,
                                    "total_area": prop.total_area,
                                    "bedrooms": prop.bedrooms
                                    })
        return request.make_response(json.dumps({"result": properties_data}), [('Content-Type', 'application/json')])

    @http.route('/properties/create_or_update_property/{property_id}', auth='public', methods=['POST'])
    def create_or_update_property(self, property_id, values):
        if not property_id:
            property = request.env['estate.property'].sudo().create(values)
            return {"result": property.id}

        property = request.env['estate.property'].sudo().search([('id','=', property_id)])
        if not property:
            property = request.env['estate.property'].sudo().create(values)
            return {"result": property.id}
        property.write(values)
        return {"result": property.id}
