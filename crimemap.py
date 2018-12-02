from dbhelper import DBHelper 
from flask import Flask, render_template, request 

app = Flask(__name__)
db = DBHelper() 

@app.route('/')
def index(): 
    try: 
        data = db.get_all_inputs() 
    except Exception as e: 
        print(e)
        data = None 
    return render_template('index.html', data=data)

@app.route('/add', methods=['POST'])
def add(): 
    try: 
        data = request.form.get('userinput')
        db.add_input(data)
    except Exception as e: 
        print(e)
    return index() 

@app.route('/clear')
def clear(): 
    try: 
        db.clear_all() 
    except Exception as e: 
        print(e)
    return index() 

if __name__ == '__main__': 
    app.run(port=4444, debug=True)