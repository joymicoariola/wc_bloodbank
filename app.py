from flask import Flask, render_template
import MySQLdb as mariadb
from flask import request, flash
from db_connector import connect_to_database, execute_query
import os

# Configuration

app = Flask(__name__)
app.secret_key = 'YAYA'

# Routes 

@app.route('/index')
@app.route('/')
def index():
    return render_template("index.j2")

# ----------------- DONORS PAGE ------------------------

@app.route('/donors')
def donors():
    db_connection = connect_to_database()
    query = "SELECT donorId, firstName, lastName, dateOfBirth, bloodType FROM Donors ORDER BY firstName ASC;"
    sql_result = execute_query(db_connection, query).fetchall()
    return render_template("donors.j2", people=sql_result)

@app.route('/donors_sort', methods=['POST', 'GET'])
def donors_sort():
    db_connection = connect_to_database()
    option = request.form['sortBy']
    if option == "firstNameSort":
        query = "SELECT donorId, firstName, lastName, dateOfBirth, bloodType FROM Donors ORDER BY firstName ASC;"
    elif option == "lastNameSort":
        query = "SELECT donorId, firstName, lastName, dateOfBirth, bloodType FROM Donors ORDER BY lastName ASC;"
    elif option == "dobSort":
        query = "SELECT donorId, firstName, lastName, dateOfBirth, bloodType FROM Donors ORDER BY dateOfBirth ASC;"
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
    if fname == '' or lname == '' or dob == '' or street == '' or city == '' or zip == '' or phone == '' or email == '':
        flash('ALERT: Please ensure all required fields are completed.')
    else:
        query = "INSERT INTO Donors (firstName, lastName, dateOfBirth, bloodType, nextDonation, lastDonation, street, city, state, zip, phone, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        data = (fname, lname, dob, btype, nextDate, lastDate, street, city, state, zip, phone, email)
        result = execute_query(db_connection, query, data)
    query = "SELECT donorId, firstName, lastName, dateOfBirth, bloodType FROM Donors ORDER BY dateOfBirth ASC;"
    sql_result = execute_query(db_connection, query).fetchall()
    return render_template("donors.j2", people=sql_result)

@app.route('/update_donor/<rowId>', methods=['POST', 'GET'])
def update_donor(rowId):
    db_connection = connect_to_database()
    query = "SELECT firstName, lastName, dateOfBirth, bloodType, nextDonation, lastDonation, street, city, state, zip, phone, email FROM Donors WHERE donorId = %s;"
    pre = execute_query (db_connection, query, [rowId]).fetchall()
    return render_template("update_donor.j2", donor_id=rowId, prePop=pre)

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
    if fname == '' or lname == '' or dob == '' or street == '' or city == '' or zip == '' or phone == '' or email == '':
        flash('ALERT: Please ensure all required fields are completed.')
    else:
        data = (fname, lname, dob, btype, nextDate, lastDate, street, city, state, zip, phone, email, rowId)
        query = "UPDATE Donors SET firstName = %s, lastName = %s, dateOfBirth = %s, bloodType = %s, nextDonation = %s, lastDonation = %s, street = %s, city = %s, state = %s, zip = %s, phone = %s, email = %s WHERE donorId = %s;"
        result = execute_query(db_connection, query, data)
    query = "SELECT donorId, firstName, lastName, dateOfBirth, bloodType FROM Donors ORDER BY firstName ASC;"
    sql_result = execute_query(db_connection, query).fetchall()
    return render_template("donors.j2", people=sql_result)

@app.route('/delete_donor/<int:id>')
def delete_donor(id):
    db_connection = connect_to_database()
    query = "DELETE FROM Donors WHERE donorID = %s"
    data = (id,)
    result = execute_query(db_connection, query, data)
    updated_query = "SELECT donorID, firstName, lastName, dateOfBirth, bloodType FROM Donors ORDER BY firstName ASC;"
    sql_result = execute_query(db_connection, updated_query).fetchall()
    return render_template("donors.j2", people=sql_result)



# ----------------- PHLEBOTOMISTS PAGE ------------------------

@app.route('/phlebotomists')
def phlebotomists():
    db_connection = connect_to_database()
    query = "SELECT DISTINCT Banks.bankName, Banks.bankID FROM Phlebotomist CROSS JOIN Banks;"
    dropDownResult = execute_query(db_connection, query).fetchall()
    query = "SELECT phlebotomistID, bankID, firstName, lastName, licenseExpiration, phone FROM Phlebotomist ORDER BY firstName ASC;"
    sql_result = execute_query(db_connection, query).fetchall()
    return render_template("phlebotomists.j2", people=sql_result, bankNames=dropDownResult)

@app.route('/add_new_phlebotomist', methods=['POST', 'GET'])
def add_new_phlebotomist():
    db_connection = connect_to_database()
    query = "SELECT DISTINCT Banks.bankName, Banks.bankID FROM Phlebotomist CROSS JOIN Banks;"
    dropDownResult = execute_query(db_connection, query).fetchall()
    fname = request.form['firstName']
    lname = request.form['lastName']
    licenseExp = request.form['licenseExpiration']
    phone = request.form['phone']
    bankID = request.form['bankID']
    if fname == '' or lname == '' or licenseExp == '' or phone == '':
        flash('ALERT: Please ensure all required fields are completed.')
    else:
        query = "INSERT INTO Phlebotomist (firstName, lastName, licenseExpiration, phone, bankID) VALUES (%s, %s, %s, %s, %s)"
        data = (fname, lname, licenseExp, phone, bankID)
        result = execute_query(db_connection, query, data)
    query = "SELECT phlebotomistID, bankID, firstName, lastName, licenseExpiration, phone FROM Phlebotomist ORDER BY firstName ASC;"
    sql_result = execute_query(db_connection, query).fetchall()
    return render_template("phlebotomists.j2", people=sql_result, bankNames=dropDownResult)

@app.route('/update_phlebotomist/<rowId>', methods=['POST', 'GET'])
def update_phlebotomist(rowId):
    db_connection = connect_to_database()
    query = "SELECT DISTINCT Banks.bankName, Banks.bankID FROM Phlebotomist CROSS JOIN Banks;"
    dropDownResult = execute_query(db_connection, query).fetchall()
    query = "SELECT bankID, firstName, lastName, licenseExpiration, phone FROM Phlebotomist WHERE phlebotomistID = %s;"
    pre = execute_query(db_connection, query, [rowId]).fetchall()
    return render_template("update_phlebotomist.j2", phlebotomist_id=rowId, prePop=pre, bankNames=dropDownResult)

@app.route('/submit_phlebotomist_update/<rowId>', methods=['POST', 'GET'])
def submit_phlebotomist_update(rowId):
    db_connection = connect_to_database()
    query = "SELECT DISTINCT Banks.bankName, Banks.bankID FROM Phlebotomist CROSS JOIN Banks;"
    dropDownResult = execute_query(db_connection, query).fetchall()
    fname = request.form['firstName']
    lname = request.form['lastName']
    licenseExp = request.form['licenseExpiration']
    phone = request.form['phone']
    bankID = request.form['bankID']
    if fname == '' or lname == '' or licenseExp == '' or phone == '':
        flash('ALERT: Please ensure all required fields are completed.')
    else:
        data = (bankID, fname, lname, licenseExp, phone, rowId)
        query = "UPDATE Phlebotomist SET bankID = %s, firstName = %s, lastName = %s, licenseExpiration = %s, phone = %s WHERE phlebotomistID = %s;"
        result = execute_query(db_connection, query, data)
    query = "SELECT phlebotomistID, bankID, firstName, lastName, licenseExpiration, phone FROM Phlebotomist ORDER BY firstName ASC;"
    sql_result = execute_query(db_connection, query).fetchall()
    return render_template("phlebotomists.j2", people=sql_result, bankNames=dropDownResult)

@app.route('/delete_phlebotomist/<int:id>')
def delete_phlebotomist(id):
    db_connection = connect_to_database()
    query = "SELECT DISTINCT Banks.bankName, Banks.bankID FROM Phlebotomist CROSS JOIN Banks;"
    dropDownResult = execute_query(db_connection, query).fetchall()
    query = "DELETE FROM Phlebotomist WHERE phlebotomistID = %s"
    data = (id,)
    result = execute_query(db_connection, query, data)
    updated_query = "SELECT phlebotomistID, bankID, firstName, lastName, licenseExpiration, phone FROM Phlebotomist ORDER BY firstName ASC;"
    sql_result = execute_query(db_connection, updated_query).fetchall()
    return render_template("phlebotomists.j2", people=sql_result, bankNames=dropDownResult)



# ----------------- SCHEDULES PAGE ------------------------

@app.route('/schedules')
def schedules():
    db_connection = connect_to_database()
    query = "SELECT DISTINCT Banks.bankName, Banks.bankID FROM Schedules CROSS JOIN Banks;"
    dropDownResult = execute_query(db_connection, query).fetchall()
    query = "SELECT scheduleID, bankID, scheduleDate, startTime, endTime FROM Schedules ORDER BY scheduleDate ASC;"
    sql_result = execute_query(db_connection, query).fetchall()
    return render_template("schedules.j2", people=sql_result, bankNames=dropDownResult)

@app.route('/add_new_schedule', methods=['POST', 'GET'])
def add_new_schedule():
    db_connection = connect_to_database()
    query = "SELECT DISTINCT Banks.bankName, Banks.bankID FROM Schedules CROSS JOIN Banks;"
    dropDownResult = execute_query(db_connection, query).fetchall()
    bankID = request.form['bankID']
    date = request.form['scheduleDate']
    startTime = request.form['startTime']
    endTime = request.form['endTime']
    if date == '' or startTime == '' or endTime == '':
        flash('ALERT: Please ensure all required fields are completed.')
    else:
        query = "INSERT INTO Schedules (bankID, scheduleDate, startTime, endTime) VALUES (%s, %s, %s, %s)"
        data = (bankID, date, startTime, endTime)
        result = execute_query(db_connection, query, data)
    query = "SELECT scheduleID, bankID, scheduleDate, startTime, endTime FROM Schedules ORDER BY scheduleDate ASC;"
    sql_result = execute_query(db_connection, query).fetchall()
    return render_template("schedules.j2", people=sql_result, bankNames=dropDownResult)

@app.route('/update_schedule/<rowId>', methods=['POST', 'GET'])
def update_schedule(rowId):
    db_connection = connect_to_database()
    query = "SELECT DISTINCT Banks.bankName, Banks.bankID FROM Phlebotomist CROSS JOIN Banks;"
    dropDownResult = execute_query(db_connection, query).fetchall()
    query = "SELECT bankID, scheduleDate, startTime, endTime FROM Schedules WHERE scheduleId = %s;"
    pre = execute_query(db_connection, query, [rowId]).fetchall()
    return render_template("update_schedule.j2", schedule_id=rowId, prePop=pre, bankNames=dropDownResult)

@app.route('/submit_schedule_update/<rowId>', methods=['POST', 'GET'])
def submit_schedule_update(rowId):
    db_connection = connect_to_database()
    query = "SELECT DISTINCT Banks.bankName, Banks.bankID FROM Phlebotomist CROSS JOIN Banks;"
    dropDownResult = execute_query(db_connection, query).fetchall()
    bankID = request.form['bankID']
    date = request.form['scheduleDate']
    startTime = request.form['startTime']
    endTime = request.form['endTime']
    if date == '' or startTime == '' or endTime == '':
        flash('ALERT: Please ensure all required fields are completed.')
    else:
        data = (bankID, date, startTime, endTime, rowId)
        query = "UPDATE Schedules SET bankID = %s, scheduleDate = %s, startTime = %s, endTime = %s WHERE scheduleId = %s;"
        result = execute_query(db_connection, query, data)
    query = "SELECT scheduleID, bankID, scheduleDate, startTime, endTime FROM Schedules ORDER BY scheduleDate ASC;"
    sql_result = execute_query(db_connection, query).fetchall()
    return render_template("schedules.j2", people=sql_result, bankNames=dropDownResult)

@app.route('/delete_schedule/<int:id>')
def delete_schedule(id):
    db_connection = connect_to_database()
    query = "SELECT DISTINCT Banks.bankName, Banks.bankID FROM Phlebotomist CROSS JOIN Banks;"
    dropDownResult = execute_query(db_connection, query).fetchall()
    query = "DELETE FROM Schedules WHERE scheduleID = %s"
    data = (id,)
    result = execute_query(db_connection, query, data)
    updated_query = "SELECT scheduleID, bankID, scheduleDate, startTime, endTime FROM Schedules ORDER BY scheduleDate ASC;"
    sql_result = execute_query(db_connection, updated_query).fetchall()
    return render_template("schedules.j2", people=sql_result, bankNames=dropDownResult)



# ----------------- BANKS PAGE ------------------------

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
    if bankName == '' or address == '' or city == '' or zip == '' or phone == '':
        flash('ALERT: Please ensure all required fields are completed.')
    else:
        query = "INSERT INTO Banks (bankName, bankAddress, city, state, zip, phone) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (bankName, address, city, state, zip, phone)
        result = execute_query(db_connection, query, data)
    query = "SELECT bankId, bankName, bankAddress, phone FROM Banks"
    sql_result = execute_query(db_connection, query).fetchall()
    return render_template("banks.j2", people=sql_result)

@app.route('/update_bank/<rowId>', methods=['POST', 'GET'])
def update_bank(rowId):
    db_connection = connect_to_database()
    query = "SELECT bankName, bankAddress, city, state, zip, phone FROM Banks WHERE bankID = %s;"
    pre = execute_query(db_connection, query, [rowId]).fetchall()
    return render_template("update_bank.j2", bank_id=rowId, prePop=pre)

@app.route('/submit_bank_update/<rowId>', methods=['POST', 'GET'])
def submit_bank_update(rowId):
    db_connection = connect_to_database()
    bankName = request.form['bankName']
    address = request.form['bankAddress']
    city = request.form['city']
    state = request.form['state']
    zip = request.form['zip']
    phone = request.form['phone']
    if bankName == '' or address == '' or city == '' or zip == '' or phone == '':
        flash('ALERT: Please ensure all required fields are completed.')
    else:
        data = (bankName, address, city, state, zip, phone, rowId)
        query = "UPDATE Banks SET bankName = %s, bankAddress = %s, city = %s, state = %s, zip = %s, phone = %s WHERE bankID = %s;"
        result = execute_query(db_connection, query, data)
    query = "SELECT bankId, bankName, bankAddress, phone FROM Banks;"
    sql_result = execute_query(db_connection, query).fetchall()
    return render_template("banks.j2", people=sql_result)

@app.route('/delete_bank/<int:id>')
def delete_bank(id):
    db_connection = connect_to_database()
    query = "DELETE FROM Banks WHERE bankID = %s"
    data = (id,)
    result = execute_query(db_connection, query, data)
    updated_query = "SELECT bankID, bankName, bankAddress, phone FROM Banks"
    sql_result = execute_query(db_connection, updated_query).fetchall()
    return render_template("banks.j2", people=sql_result)



# ----------------- DONATIONS PAGE ------------------------

@app.route('/add_new_donations', methods=['POST', 'GET'])
def add_new_donations():
    db_connection = connect_to_database()
    scheduleID = request.form['scheduleID']
    phlebotomistID = request.form['phlebotomistID']
    donorID = request.form['donorID']
    if scheduleID == '' or phlebotomistID == '' or donorID == '':
        flash('ALERT: Please ensure all required fields are completed.')
    else:
        query = "INSERT INTO Donations (donorID, phlebotomistID, scheduleID) VALUES (%s, %s, %s)"
        data = (scheduleID, phlebotomistID, donorID)
        result = execute_query(db_connection, query, data)
    query = "SELECT scheduleID, phlebotomistID, donorID FROM Donations"
    sql_result = execute_query(db_connection, query).fetchall()
    return render_template("donations.j2", people=sql_result)

@app.route('/delete_donations', methods=['POST', 'GET'])
def delete_donations():
    db_connection = connect_to_database()
    scheduleID = request.form['scheduleID']
    phlebotomistID = request.form['phlebotomistID']
    donorID = request.form['donorID']
    if scheduleID == '' or phlebotomistID == '' or donorID == '':
        flash('ALERT: Please ensure all required fields are completed.')
    else:
        query = "DELETE FROM Donations WHERE donorID = %s AND phlebotomistID = %s AND scheduleID = %s"
        data = (donorID, phlebotomistID, scheduleID)
        result = execute_query(db_connection, query, data)
    updated_query = "SELECT donorID, phlebotomistID, scheduleID FROM Donations"
    sql_result = execute_query(db_connection, updated_query).fetchall()
    return render_template("donations.j2", people=sql_result)

@app.route('/donations')
def donations():
    db_connection = connect_to_database()
    query = "SELECT scheduleID, phlebotomistID, donorID FROM Donations"
    sql_result = execute_query(db_connection, query).fetchall()
    return render_template("donations.j2", people=sql_result)


# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 6825))
    app.run(host="flip1.engr.oregonstate.edu", port=port, debug=True)
