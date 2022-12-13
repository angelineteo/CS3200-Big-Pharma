from flask import Blueprint, request, jsonify, make_response, app
import json

from flaskext.mysql import MySQL

db = MySQL()
db.init_app(app)
insurers_blueprint = Blueprint('insurers', __name__)

# Get all insurers' ids and names from the DB
@insurers_blueprint.route('/customers', methods=['GET'])
def get_insurers():
    cursor = db.get_db().cursor()
    cursor.execute('select IID, name, firstName, from INSURER_DATA')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# Get the insurer profile page
@insurers_blueprint.route('/<id>/profile', methods=['GET'])
def get_in_profile(id):
    cursor = db.get_db().cursor()
    cursor.execute('select i.name, i.street, i.city, i.zip, i.country, i.phoneNum\
                   from INSURER_DATA i'
                   'where IID = {0}'.format(id))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get the insurer coverage page
@insurers_blueprint.route('/<id>/coverage', methods=['GET'])
def get_in_coverage(id):
    cursor = db.get_db().cursor()
    cursor.execute('select p.name\
                   from INSURER_DATA i JOIN PRODUCT_DATA p on i.IID == p.insurance_ID'
                   'where i.IID = {0}'.format(id))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# look up a specific drug on insurance coverage page
@insurers_blueprint.route('/<id>/coverage/<name>', methods=['POST'])
def get_in_coverage_n(id):
    name = request.form['name']
    cursor = db.get_db().cursor()
    cursor.execute('select p.name\
                   from INSURER_DATA i JOIN PRODUCT_DATA p on i.IID == p.insurance_ID'
                   f'where p.name == {name}''and i.IID = {0}'.format(id))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
