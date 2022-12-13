from flask import Blueprint, request, jsonify, make_response, app
import json

from flaskext.mysql import MySQL

db = MySQL()
db.init_app(app)
manufacturers_blueprint = Blueprint('manufacturers', __name__)


# Get all manufacturers' ids and names from the DB
@manufacturers_blueprint.route('/manufacturers', methods=['GET'])
def get_manufacturers():
    cursor = db.get_db().cursor()
    cursor.execute('select id, name, from MANUFACTURER_DATA')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get the manufacturer contact page
@manufacturers_blueprint.route('/<id>/contact', methods=['GET'])
def get_man_contact(id):
    cursor = db.get_db().cursor()
    cursor.execute('select m.id, m.name, m.street, m.city, m.zip, m.state, m.phoneNum\
                   from MANUFACTURER_DATA m'
                   'where m.id = {0}'.format(id))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get the manufacturer product page
@manufacturers_blueprint.route('/<id>/coverage', methods=['GET'])
def get_man_products(id):
    cursor = db.get_db().cursor()
    cursor.execute('select p.name, i.name, p.productID\
                   from MANUFACTURER_DATA m JOIN PRODUCT_DATA p on m.id == p.m_id JOIN '
                   'INGREDIENTS_DATA g on p.productID == g.product_ID'
                   'where m.id = {0}'.format(id))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response