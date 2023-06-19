#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Planet, Scientist, Mission

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)



db.init_app(app)

api = Api(app)

@app.route('/')
def home():
    return ''

class Scientists(Resource):
    def get(self):
        all_scientists = Scientist.query.all()
        scientists_list = [s.to_json() for s in all_scientists]
        response = make_response(scientists_list, 200)
        return response
    
    def post(self):
        data = request.get_json()

        new_scientist = Scientist(
            name = data.get('name'),
            field_of_study = data.get('field_of_study'),
            avatar = data.get('avatar')
        )

        db.session.add(new_scientist)
        db.session.commit()

        response = make_response(new_scientist.to_dict(), 201)

        return response
    
api.add_resource(Scientists, '/scientists')

class ScientistByID(Resource):
    def get(self, id):

        scientist = Scientist.query.filter_by(Scientist.id == id).first()

        if  not scientist:
            return make_response(404, 'Scientist not found')

        response = make_response(scientist.to_dict(), 200)

        return response
    
    def patch(self, id):

        scientist = Scientist.query.filter_by(Scientist.id == id).first()

        if  not scientist:
            return make_response(404, 'Scientist not found')

        data = request.get_json()

        for attr in data:
            setattr(scientist, attr, data.get(attr))

        db.session.add(scientist)
        db.session.commit()

        response = make_response(scientist.to_dict(), 202)

        return response
    
    def delete(self, id):
        scientist = Scientist.query.filter_by(Scientist.id == id).first()

        if  not scientist:
            return make_response(404, 'Scientist not found')
        
        db.session.delete(scientist)
        db.session.commit()

        return make_response({}, 204)
    

    
api.add_resource(ScientistByID, '/scientist/<int:id>')



class Planets(Resource):
    def get(self, id):
        all_planets = Planet.query.all()

        planet_dict = [p.to_dict() for p in all_planets]

        response = make_response(planet_dict, 200)

        return response
    
api.add_resource(Planets, '/planets')


class Missions(Resource):
    def post(self):

        data = request.get_json()

        new_mission = Mission(
            name = data.get('name'),
            scientist_id = data.get('scientist_id'),
            planet_id = data.get('planet_id')
        )

        db.session.add(new_mission)
        db.session.commit()

        response = make_response(new_mission.to_dict(), 201)

        return response
    
api.add_resource(Mission, '/missions')

        


if __name__ == '__main__':
    app.run(port=5555, debug=True)
