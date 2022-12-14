###
# Main application interface
###

# import the create app function 
# that lives in src/__init__.py
from src import create_app

# create the app object
app = create_app()

if __name__ == '__main__':
    # we want to run in debug mode (for hot reloading) 
    # this app will be bound to port 4000. 
    # Take a look at the docker-compose.yml to see 
    # what port this might be mapped to... 
    app.run(debug = True, host = '0.0.0.0', port = 4000)# Some set up for the application

from flask import Flask, jsonify, request
from flaskext.mysql import MySQL


app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE-PORT'] = 3306
app.config['MYSQL_DATABASE_USER'] = 'webapp'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Bdfap738GHf'
app.config['MYSQL_DATABASE_DB'] = 'pharmacy'

db_conn = MySQL()
db_conn.init_app(app)


@app.route('/testdb')
def test_db():
    cur = db_conn.get_db().cursor()
    cur.execute('SELECT * FROM MANUFACTURER_DATA')
    col_header = [y[0] for y in cur.description]
    json_data = []
    the_data = cur.fetchall()
    for row in the_data:
        json_data.append(dict(zip(col_header, row)))
    return jsonify(json_data)


@app.route('/customers', methods=['GET'])
def get_customers():
    cursor = db_conn.get_db().cursor()
    cursor.execute('select cust_id, lastName, firstName from CUST_DATA')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    thedata = cursor.fetchall()
    for row in thedata:
        json_data.append(dict(zip(row_headers, row)))
    return jsonify(json_data)


@app.route('/<userID>/profile', methods=['GET'])
def get_cust_pro(userID):
    cursor = db_conn.get_db().cursor()
    cursor.execute('select c.firstName, c.lastName, c.bday, c.phoneNum, c.street, c.city, c.zip, c.country, i.name\
                   from CUST_DATA c JOIN INSURER_DATA i ON c.insuranceID = i.IID\
                   where cust_ID = {0}'.format(userID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    return jsonify(json_data)


@app.route('/drug-lookup', methods=['GET'])
def get_cust_lookup():
    cursor = db_conn.get_db().cursor()
    cursor.execute('SELECT name FROM PRODUCT_DATA ORDER BY name')
    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers.
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)


@app.route('/drug_lookup/<name>', methods=['GET'])
def get_in_coverage_n(name):
    cursor = db_conn.get_db().cursor()
    cursor.execute('select * from PRODUCT_DATA p where p.name = "{0}"'.format(name))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    return jsonify(json_data)


@app.route('/insurer/customers', methods=['GET'])
def get_insurers():
    cursor = db_conn.get_db().cursor()
    cursor.execute('select IID, name from INSURER_DATA')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    return jsonify(json_data)


@app.route('/insurer/<id>/profile', methods=['GET'])
def get_in_profile(id):
    cursor = db_conn.get_db().cursor()
    cursor.execute('select i.name, i.street, i.city, i.zip, i.country, i.phoneNum\
                   from INSURER_DATA i where IID = {0}'.format(id))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    return jsonify(json_data)


@app.route('/insurer/<id>/coverage', methods=['GET'])
def get_in_coverage(id):
    cursor = db_conn.get_db().cursor()
    cursor.execute('select p.name\
                   from INSURER_DATA i JOIN PRODUCT_DATA p ON i.IID = p.insurance_ID '
                   'where i.IID = {0}'.format(id))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    return jsonify(json_data)


@app.route('/manufacturers', methods=['GET'])
def get_manufacturers():
    cursor = db_conn.get_db().cursor()
    cursor.execute('select id, name from MANUFACTURER_DATA')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    return jsonify(json_data)


@app.route('/<iid>/contact', methods=['GET'])
def get_man_contact(iid):
    cursor = db_conn.get_db().cursor()
    cursor.execute('select id, name, street, city, zip, state, phoneNum\
                   from MANUFACTURER_DATA '
                   'where id = {0}'.format(iid))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    return jsonify(json_data)


# Get the manufacturer product page
@app.route('/manufacturer/<mid>/coverage', methods=['GET'])
def get_man_products(mid):
    cursor = db_conn.get_db().cursor()
    cursor.execute('select p.name, g.name, p.productID\
                   from MANUFACTURER_DATA m JOIN PRODUCT_DATA p on m.id = p.m_id JOIN '
                   'INGREDIENT_DATA g ON p.productID = g.product_ID '
                   'where m.id = {0}'.format(mid))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    return jsonify(json_data)


@app.route('/products', methods=['GET'])
def get_products():
    # get a cursor object from the database
    cursor = db_conn.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute('select p.name, m.name as manufacturer from PRODUCT_DATA p JOIN MANUFACTURER_DATA m ON'
                   ' p.m_id = m.id')

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


@app.route('/login', methods=['POST'])
def login():
    app.logger.info(request.form)
    userid = request.form['userid']
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    cursor = db_conn.get_db().cursor()
    cursor.execute(f'select * from CUST_DATA where cust_id = \"{userid}\" AND firstName = \"{firstName}"'
                   f' AND lastName = \"{lastName}\"')
    return "Welcome!"


@app.route('/')
def base_route():
    return '<h1> This is the base route </h1>'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)

