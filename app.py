from flask import Flask, render_template
import MySQLdb as mariadb
from db_credentials import host, user, passwd, db
import os

# Configuration

app = Flask(__name__)

people_from_app_py = [
{
    "name": "Thomas",
    "age": 33,
    "location": "New Mexico",
    "favorite_color": "Blue"
},
{
    "name": "Gregory",
    "age": 41,
    "location": "Texas",
    "favorite_color": "Red"
},
{
    "name": "Vincent",
    "age": 27,
    "location": "Ohio",
    "favorite_color": "Green"
},
{
    "name": "Alexander",
    "age": 29,
    "location": "Florida",
    "favorite_color": "Orange"
}]

# Routes 

@app.route('/index')
@app.route('/')
def index():
    return render_template("index.j2")

@app.route('/donations')
def donations():
    return render_template("donations.j2", people=people_from_app_py)

@app.route('/donors')
def donors():
    return render_template("donors.j2", people=people_from_app_py)

@app.route('/schedules')
def schedules():
    return render_template("schedules.j2", people=people_from_app_py)

@app.route('/banks')
def banks():
    return render_template("banks.j2", people=people_from_app_py)

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 7984))
    app.run(host="flip1.engr.oregonstate.edu", port=port, debug=True) 