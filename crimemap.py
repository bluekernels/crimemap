from dbhelper import DBHelper 
from flask import Flask, render_template, request 
import json 

app = Flask(__name__)
db = DBHelper() 

@app.route('/')
def index():
    crimes = db.get_all_crimes() 
    crimes = json.dumps(crimes)
    print(crimes)
    return render_template('index.html', crimes=crimes)

@app.route('/reportcrime', methods=['POST'])
def reportcrime(): 
    category = request.form.get('category')
    date = request.form.get('date')
    latitude = float(request.form.get('latitude'))
    longitude = float(request.form.get('longitude'))
    description = request.form.get('description')
    db.add_crime(category, date, latitude, longitude, description)
    return index() 
if __name__ == '__main__': 
    app.run(port=4444, debug=True)