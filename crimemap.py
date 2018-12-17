from dbhelper import DBHelper 
from flask import Flask, render_template, request 
import json 
import datetime 
import dateparser  
import cgi 
import sqreen

sqreen.start()
app = Flask(__name__)
db = DBHelper() 
categories = ["Larceny","Robbery","Burglary","Arson","Embezzlement","Forgery","False pretense","Kidnapping","Homicide","Rape"]
@app.route('/')
def index(error_message=None):
    crimes = db.get_all_crimes() 
    crimes = json.dumps(crimes)
    print(crimes)
    return render_template('index.html', crimes=crimes,categories=categories, error_message=error_message)

@app.route('/reportcrime', methods=['POST'])
def reportcrime(): 
    category = request.form.get('category')
    if category not in categories:
        return index() 
    date = format_date(request.form.get('date'))
    if not date:
        return index("Invalid date. Plese use yyyy-mm-dd format")
    try: 
        latitude = float(request.form.get('latitude'))
        longitude = float(request.form.get('longitude'))
    except ValueError: 
        return index() 
    description = sanitize(request.form.get('description'))
    db.add_crime(category, date, latitude, longitude, description)
    return index() 

def format_date(userdate):
    date = dateparser.parse(userdate)
    try:
        return datetime.datetime.strftime(date, "%Y-%m-%d")
    except TypeError:
        return None 

def sanitize(userinput):
    transform = cgi.escape(userinput)
    return transform 
def sanitize_string(userinput): 
    whitelist = string.ascii_letters + string.digits + " !?$.,;:-'()&"
    return filter(lambda x: x in whitelist, userinput)
if __name__ == '__main__': 
    app.run(port=4444, debug=True)