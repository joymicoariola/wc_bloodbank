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

@app.route('/Phlebotomists')
def phlebotomists():
    return render_template("phlebotomists.j2")

@app.route('/schedules')
def schedules():
    return render_template("schedules.j2")

@app.route('/banks')
def banks():
    return render_template("banks.j2")

@app.route('/donors_schedules')
def donors_schedules():
    return render_template("donors_schedules.j2")

@app.route('/phlebotomists_schedules')
def phlebotomists_schedules():
    return render_template("phlebotomists_schedules.j2")

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 7980))
    app.run(host="flip1.engr.oregonstate.edu", port=port, debug=True) 