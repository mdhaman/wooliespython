import flask
import functools
import json
import time
from datetime import datetime
from copy import deepcopy
from enum import Enum
from woolies.api import blueprint
from flask import current_app, jsonify, abort, make_response


class SortOtpions(Enum):
    High = 'High'
    Low = 'Low'
    Ascending = 'Ascending'
    Descending = 'Descending'
    Recommended = 'Recommended'

@blueprint.route('/answers/user', methods=['GET'])
def user():
    return jsonify({'token': current_app.config.get('TOKEN'), 'name': 'Mayur Dhamanwala'})


@blueprint.route('/answers/sort', methods=['GET'])
def sort():
    products = current_app.woolies_api.get_products()
    sort_option = flask.request.args.get('sortOption')
    if not sort_option:
        abort(400)
    
    if sort_option.lower() == SortOtpions.Low.value.lower():
        return jsonify(sorted(products, key=lambda p: p.get('price')))
    elif sort_option.lower() == SortOtpions.High.value.lower():
        return jsonify(sorted(products, key=lambda p: p.get('price'), reverse=True))
    elif sort_option.lower() == SortOtpions.Ascending.value.lower():
        return jsonify(sorted(products, key=lambda p: p.get('name')))
    elif sort_option.lower() == SortOtpions.Descending.value.lower():
        return jsonify(sorted(products, key=lambda p: p.get('name'), reverse=True))
    elif sort_option.lower() == SortOtpions.Recommended.value.lower():
        shopper_history = current_app.woolies_api.get_shopper_history();

        shopper_products = {}
        for history in shopper_history:
            for product in history.get('products'):
                if product.get('name') not in shopper_products:
                    shopper_products[product.get('name')] = product.get('quantity')
                else:
                    shopper_products[product.get('name')] = shopper_products[product.get('name')] + product.get('quantity')

        def compare(p1, p2):
            p1_quantity = shopper_products.get(p1.get('name'))
            p2_quantity = shopper_products.get(p2.get('name'))

            if (p1_quantity and p2_quantity):
                return p2_quantity - p1_quantity
            
            if p1_quantity:
                return -1

            if p2_quantity:
                return 1

            return 0

        return jsonify(sorted(products, key=functools.cmp_to_key(compare)))

@blueprint.route('/answers/trolleyTotal', methods=['GET', 'POST'])
def trolley():
    data = flask.request.get_json()
    product_lookup = {p['Name']: p['Price'] for p in data.get('Products', [])}
    quantity_lookup = {q['Name']: q['Quantity'] for q in data.get('Quantities', [])}
    totals = [sum([p['Price'] * quantity_lookup.get(p['Name'], 0.0) for p in data.get('Products') or []])]

    def is_valid_quantity(quantities=[], lookup={}):
        for quantity in quantities:
            if not lookup.get(quantity.get('Name')) is None and lookup.get(quantity.get('Name')) < quantity.get('Quantity'):
                return False
        return True

    for special in data.get('Specials', []):
        if is_valid_quantity(special.get('Quantities', []), quantity_lookup):
            new_quantity = deepcopy(quantity_lookup)
            special_quantity = {q['Name']: q['Quantity'] for q in special.get('Quantities', [])}
            count = 0
            while(is_valid_quantity(special.get('Quantities', []), new_quantity)):
                count += 1
                for name, quantity in special_quantity.items():
                    new_quantity[name] = new_quantity[name] - quantity

            totals.append((count * special.get('Total')) + sum([(new_quantity[key] * product_lookup[key]) for key in new_quantity.keys()]))
    return make_response(jsonify(min(totals)), 200)
