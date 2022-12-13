from flask import Blueprint, request, jsonify, make_response
import json
from src import db


customers = Blueprint('customers', __name__)

# Get all customers' ids, first, and last names from the DB
@customers_blueprint.route('/customers', methods=['GET'])
def get_customers():
    cursor = db.get_db().cursor()
    cursor.execute('select cust_id, lastName, firstName,\
        from CUST_DATA')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get the customer profile page
@customers_blueprint.route('/<userID>/profile', methods=['GET'])
def get_cust_pro(userID):
    cursor = db.get_db().cursor()
    cursor.execute('select c.firstName, c.lastName, c.bday, c.phoneNum, c.street, c.city, c.zip, c.country, i.name\
                   from CUST_DATA c NATURAL JOIN INSURER_DATA i \
                   where customerID = {0}'.format(userID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

#gets all the drugs available to customers - shows top 5 alphabetized
@customers_blueprint.route('/drug-lookup', methods=['GET'])
def get_cust_lookup():
    cursor = db.get_db().cursor()
    query = '''
            SELECT p.name
            FROM products p
            ORDER BY name DESC
            LIMIT 5;
        '''
    cursor.execute(query)
    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers.
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)

# look up a specific drug on a customers lookup page
@customers_blueprint.route('/drug_lookup/<name>', methods=['POST'])
def get_in_coverage_n(id):
    name = request.form['name']
    cursor = db.get_db().cursor()
    cursor.execute(f'select p.name\
                   from PRODUCT_DATA\
                   where p.name == {name}')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
