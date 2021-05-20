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
    query = "SELECT firstName, lastName, dateOfBirth, bloodType FROM Donors ORDER BY firstName ASC;"
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
    return render_template("donors.j2")

@app.route('/phlebotomists')
def phlebotomists():
    db_connection = connect_to_database()
    query = "SELECT bankID, firstName, lastName, licenseExpiration FROM Phlebotomist"
    sql_result = execute_query(db_connection, query).fetchall()
    return render_template("phlebotomists.j2", people=sql_result)

@app.route('/schedules')
def schedules():
    db_connection = connect_to_database()
    query = "SELECT scheduleDate, startTime, endTime FROM Schedules"
    sql_result = execute_query(db_connection, query).fetchall()
    return render_template("schedules.j2", people=sql_result)

@app.route('/banks')
def banks():
    db_connection = connect_to_database()
    query = "SELECT bankName, bankAddress, phone FROM Banks"
    sql_result = execute_query(db_connection, query).fetchall()
    return render_template("banks.j2", people=sql_result)

@app.route('/donations')
def donations():
    db_connection = connect_to_database()
    query = "SELECT scheduleID, phlebotomistID, donorID FROM Donations"
    sql_result = execute_query(db_connection, query).fetchall()
    return render_template("donations.j2", people=sql_result)
# Listener

if __name__ == "__main__":
    app.run() 