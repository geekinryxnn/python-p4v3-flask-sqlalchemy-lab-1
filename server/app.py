# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def  get_earthquake_by_id(id):
    result = Earthquake.query.filter(Earthquake.id == id).first()
    if result:
        response_body = jsonify({
        "id": result.id,
        "location": result.location,
         "magnitude": result.magnitude,
         "year": result.year
        })
        status_code = 200
    else:
        response_body = jsonify({
            "message": "Earthquake 9999 not found."
        })
        status_code = 404
    headers = {}
    return make_response(response_body, status_code, headers)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquake_by_magnitude(magnitude):
    result =Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    quakes = []
    for quake in result:
        quakes.append({
            "id": quake.id,
            "location": quake.location,
            "magnitude": quake.magnitude,
            "year": quake.year
        })
        
    response_body = jsonify({
        "count": len(quakes),
        "quakes": quakes
    })
    status_code = 200
    headers = {}
    return make_response(response_body, status_code, headers)
    
if __name__ == '__main__':
    app.run(port=5555, debug=True)