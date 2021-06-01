from flask import Flask, render_template
import MySQLdb as mariadb
from flask import request
from db_connector import connect_to_database, execute_query
import os

# Configuration

app = Flask(__name__)

# Routes 

@app.route('/index')
@app.route('/')
def index():
    return render_template("index.j2")

@app.route('/donors')
def donors():
    db_connection = connect_to_database()
    query = "SELECT donorId, firstName, lastName, dateOfBirth, bloodType FROM Donors ORDER BY firstName ASC;"
    sql_result = execute_query(db_connection, query).fetchall()
    return render_template("donors.j2", people=sql_result)

@app.route('/donors_last')
def donors_last():
    db_connection = connect_to_database()
    query = "SELECT firstName, lastName, dateOfBirth, bloodType FROM Donors ORDER BY lastName ASC;"
    sql_result = execute_query(db_connection, query).fetchall()
    return render_template("donors.j2", people=sql_result)

@app.route('/donors_DOB')
def donors_DOB():
    db_connection = connect_to_database()
    query = "SELECT firstName, lastName, dateOfBirth, bloodType FROM Donors ORDER BY dateOfBirth ASC;"
    sql_result = execute_query(db_connection, query).fetchall()
    return render_template("donors.j2", people=sql_result)

@app.route('/add_new_donor', methods=['POST', 'GET'])
def add_new_donor():
    db_connection = connect_to_database()
    fname = request.form['firstName']
    lname = request.form['lastName']
    dob = request.form['dateOfBirth']
    btype = request.form['bloodType']
    nextDate = request.form['nextDonationDate']
    lastDate = request.form['lastDonationDate']
    street = request.form['street']
    city = request.form['city']
    state = request.form['state']
    zip = request.form['zip']
    phone = request.form['phone']
    email = request.form['email']
    query = "INSERT INTO Donors (firstName, lastName, dateOfBirth, bloodType, nextDonation, lastDonation, street, city, state, zip, phone, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data = (fname, lname, dob, btype, nextDate, lastDate, street, city, state, zip, phone, email)
    result = execute_query(db_connection, query, data)
    return render_template("donors.j2", people=data)

@app.route('/update_donor/<rowId>', methods=['POST', 'GET'])
def update_donor(rowId):
    db_connection = connect_to_database()
    return render_template("update_donor.j2", donor_id=rowId)

@app.route('/submit_donor_update/<rowId>', methods=['POST', 'GET'])
def submit_donor_update(rowId):
    db_connection = connect_to_database()
    fname = request.form['firstName']
    lname = request.form['lastName']
    dob = request.form['dateOfBirth']
    btype = request.form['bloodType']
    nextDate = request.form['nextDonationDate']
    lastDate = request.form['lastDonationDate']
    street = request.form['street']
    city = request.form['city']
    state = request.form['state']
    zip = request.form['zip']
    phone = request.form['phone']
    email = request.form['email']
    data = (fname, lname, dob, btype, nextDate, lastDate, street, city, state, zip, phone, email, rowId)
    query = "UPDATE Donors SET firstName = %s, lastName = %s, dateOfBirth = %s, bloodType = %s, nextDonation = %s, lastDonation = %s, street = %s, city = %s, state = %s, zip = %s, phone = %s, email = %s WHERE donorId = %s;"
    result = execute_query(db_connection, query, data)
    query = "SELECT donorId, firstName, lastName, dateOfBirth, bloodType FROM Donors ORDER BY firstName ASC;"
    sql_result = execute_query(db_connection, query).fetchall()
    return render_template("donors.j2", people=sql_result)





@app.route('/phlebotomists')
def phlebotomists():
    db_connection = connect_to_database()
    query = "SELECT phlebotomistID, bankID, firstName, lastName, licenseExpiration FROM Phlebotomist ORDER BY firstName ASC;"
    sql_result = execute_query(db_connection, query).fetchall()
    return render_template("phlebotomists.j2", people=sql_result)

@app.route('/add_new_phlebotomist', methods=['POST', 'GET'])
def add_new_phlebotomist():
    db_connection = connect_to_database()
    fname = request.form['firstName']
    lname = request.form['lastName']
    licenseExp = request.form['licenseExpiration']
    phone = request.form['phone']
    bankID = request.form['bankID']
    query = "INSERT INTO Phlebotomist (firstName, lastName, licenseExpiration, phone, bankID) VALUES (%s, %s, %s, %s, %s)"
    data = (fname, lname, licenseExp, phone, bankID)
    result = execute_query(db_connection, query, data)
    query = "SELECT phlebotomistID, bankID, firstName, lastName, licenseExpiration FROM Phlebotomist ORDER BY firstName ASC;"
    sql_result = execute_query(db_connection, query).fetchall()
    return render_template("phlebotomists.j2", people=sql_result)

@app.route('/update_phlebotomist/<rowId>', methods=['POST', 'GET'])
def update_phlebotomist(rowId):
    db_connection = connect_to_database()
    return render_template("update_phlebotomist.j2", phlebotomist_id=rowId)

@app.route('/submit_phlebotomist_update/<rowId>', methods=['POST', 'GET'])
def submit_phlebotomist_update(rowId):
    db_connection = connect_to_database()
    fname = request.form['firstName']
    lname = request.form['lastName']
    licenseExp = request.form['licenseExpiration']
    phone = request.form['phone']
    bankID = request.form['bankID']
    data = (bankID, fname, lname, licenseExp, phone, rowId)
    query = "UPDATE Phlebotomist SET bankID = %s, firstName = %s, lastName = %s, licenseExpiration = %s, phone = %s WHERE phlebotomistID =%s;"
    result = execute_query(db_connection, query, data)
    query = "SELECT phlebotomistID bankID, firstName, lastName, licenseExpiration, phone FROM Phlebotomist ORDER BY firstName ASC;"
    sql_result = execute_query(db_connection, query).fetchall()
    return render_template("donors.j2", people=sql_result)





@app.route('/schedules')
def schedules():
    db_connection = connect_to_database()
    query = "SELECT scheduleID, bankID, scheduleDate, startTime, endTime FROM Schedules ORDER BY scheduleDate ASC;"
    sql_result = execute_query(db_connection, query).fetchall()
    return render_template("schedules.j2", people=sql_result)

@app.route('/add_new_schedule', methods=['POST', 'GET'])
def add_new_schedule():
    db_connection = connect_to_database()
    date = request.form['scheduleDate']
    startTime = request.form['startTime']
    endTime = request.form['endTime']
    query = "INSERT INTO Schedules (scheduleDate, startTime, endTime) VALUES (%s, %s, %s)"
    data = (date, startTime, endTime)
    result = execute_query(db_connection, query, data)
    query = "SELECT scheduleID, bankID, scheduleDate, startTime, endTime FROM Schedules ORDER BY scheduleDate ASC;"
    sql_result = execute_query(db_connection, query).fetchall()
    return render_template("schedules.j2", people=sql_result)

@app.route('/update_schedule/<rowId>', methods=['POST', 'GET'])
def update_schedule(rowId):
    db_connection = connect_to_database()
    return render_template("update_schedule.j2", schedule_id=rowId)

@app.route('/submit_schedule_update/<rowId>', methods=['POST', 'GET'])
def submit_schedule_update(rowId):
    db_connection = connect_to_database()
    date = request.form['scheduleDate']
    startTime = request.form['startTime']
    endTime = request.form['endTime']
    data = (date, startTime, endTime, rowId)
    query = "UPDATE Schedules SET scheduleDate = %s, startTime = %s, endTime = %s WHERE scheduleId = %s;"
    result = execute_query(db_connection, query, data)
    query = "SELECT scheduleID, bankID, scheduleDate, startTime, endTime FROM Schedules ORDER BY scheduleDate ASC;"
    sql_result = execute_query(db_connection, query).fetchall()
    return render_template("schedules.j2", people=sql_result)



@app.route('/banks')
def banks():
    db_connection = connect_to_database()
    query = "SELECT bankId, bankName, bankAddress, phone FROM Banks"
    sql_result = execute_query(db_connection, query).fetchall()
    return render_template("banks.j2", people=sql_result)

@app.route('/add_new_banks', methods=['POST', 'GET'])
def add_new_banks():
    db_connection = connect_to_database()
    bankName = request.form['bankName']
    address = request.form['bankAddress']
    city = request.form['city']
    state = request.form['state']
    zip = request.form['zip']
    phone = request.form['phone']
    query = "INSERT INTO Banks (bankName, bankAddress, city, state, zip, phone) VALUES (%s, %s, %s, %s, %s, %s)"
    data = (bankName, address, city, state, zip, phone)
    result = execute_query(db_connection, query, data)
    query = "SELECT bankId, bankName, bankAddress, phone FROM Banks"
    sql_result = execute_query(db_connection, query).fetchall()
    return render_template("banks.j2", people=sql_result)

@app.route('/update_bank/<rowId>', methods=['POST', 'GET'])
def update_bank(rowId):
    db_connection = connect_to_database()
    return render_template("update_bank.j2", bank_id=rowId)

@app.route('/submit_bank_update/<rowId>', methods=['POST', 'GET'])
def submit_bank_update(rowId):
    db_connection = connect_to_database()
    bankName = request.form['bankName']
    address = request.form['bankAddress']
    city = request.form['city']
    state = request.form['state']
    zip = request.form['zip']
    phone = request.form['phone']
    data = (bankName, address, city, state, zip, phone, rowId)
    query = "UPDATE Banks SET bankName = %s, bankAddress = %s, city = %s, state = %s, zip = %s, phone = %s WHERE bankID = %s;"
    result = execute_query(db_connection, query, data)
    query = "SELECT bankId, bankName, bankAddress, phone FROM Banks;"
    sql_result = execute_query(db_connection, query).fetchall()
    return render_template("banks.j2", people=sql_result)





@app.route('/add_new_donations', methods=['POST', 'GET'])
def add_new_donations():
    db_connection = connect_to_database()
    scheduleID = request.form['scheduleID']
    phlebotomistID = request.form['phlebotomistID']
    donorID = request.form['donorID']
    query = "INSERT INTO Donations (scheduleID, phlebotomistID, donorID) VALUES (%s, %s, %s)"
    data = (scheduleID, phlebotomistID, donorID)
    result = execute_query(db_connection, query, data)
    return render_template("donations.j2")

@app.route('/donations')
def donations():
    db_connection = connect_to_database()
    query = "SELECT scheduleID, phlebotomistID, donorID FROM Donations"
    sql_result = execute_query(db_connection, query).fetchall()
    return render_template("donations.j2", people=sql_result)
# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 7982))
    app.run(host="flip1.engr.oregonstate.edu", port=port, debug=True)
