# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
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
def earthquake_by_id(id):
    earthquake = Earthquake.query.filter_by(id=id).first()

    if earthquake:
        response = make_response(
            earthquake.to_dict(),
            200
        )
    else:
        response = make_response(
            {'message': f'Earthquake {id} not found.'},
            404
        )

    return response


@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquakes_by_mag(magnitude):
    earthquakes = [earthquake.to_dict() for earthquake in 
                   Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()]
    count = len(earthquakes)


    response = make_response(
        {'count': count, 'quakes': earthquakes},
        200
    )
  

    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
