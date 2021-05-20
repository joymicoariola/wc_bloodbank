from flask import Flask, render_template
import MySQLdb as mariadb
#from db_credentials import host, user, passwd, db
import os

# Configuration

app = Flask(__name__)

people_from_app_py = [
{
    "name": "--",
    "age": 33,
    "location": "--",
    "favorite_color": "--"
},
{
    "name": "--",
    "age": 41,
    "location": "--",
    "favorite_color": "--"
},
{
    "name": "--",
    "age": 27,
    "location": "--",
    "favorite_color": "--"
},
{
    "name": "--",
    "age": 29,
    "location": "--",
    "favorite_color": "--"
}]

# Routes 

@app.route('/index')
@app.route('/')
def index():
    return render_template("index.j2")

@app.route('/donors')
def donors():
    return render_template("donors.j2", people=people_from_app_py)

@app.route('/Phlebotomists')
def phlebotomists():
    return render_template("phlebotomists.j2", people=people_from_app_py)

@app.route('/schedules')
def schedules():
    return render_template("schedules.j2", people=people_from_app_py)

@app.route('/banks')
def banks():
    return render_template("banks.j2", people=people_from_app_py)

@app.route('/donors_schedules')
def donors_schedules():
    return render_template("donors_schedules.j2", people=people_from_app_py)

@app.route('/phlebotomists_schedules')
def donors_schedules():
    return render_template("phlebotomists_schedules.j2", people=people_from_app_py)

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 7985))
    app.run(host="flip1.engr.oregonstate.edu", port=port, debug=True) 