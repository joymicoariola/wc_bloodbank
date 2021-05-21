from flask import Flask, render_template
import MySQLdb as mariadb
#from db_credentials import host, user, passwd, db
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
    return render_template("donors.j2")

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
    return render_template("donors.j2")

@app.route('/phlebotomists')
def phlebotomists():
    return render_template("phlebotomists.j2")

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
    return render_template("phlebotomists.j2")

@app.route('/schedules')
def schedules():
    return render_template("schedules.j2")

@app.route('/add_new_schedule', methods=['POST', 'GET'])
def add_new_schedule():
    db_connection = connect_to_database()
    date = request.form['scheduleDate']
    startTime = request.form['startTime']
    endTime = request.form['endTime']
    query = "INSERT INTO Schedules (scheduleDate, startTime, endTime) VALUES (%s, %s, %s)"
    data = (date, startTime, endTime)
    result = execute_query(db_connection, query, data)
    return render_template("schedules.j2")

@app.route('/banks')
def banks():
    return render_template("banks.j2")

@app.route('/banks', methods=['POST', 'GET'])
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
    return render_template("banks.j2")

@app.route('/donations')
def donations():
    return render_template("donations.j2")

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

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 7980))
    app.run(host="flip1.engr.oregonstate.edu", port=port, debug=True) 