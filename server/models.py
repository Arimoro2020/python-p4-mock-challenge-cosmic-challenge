from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
  "ix": "ix_%(column_0_label)s",
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    serialize_rules = ('-missions.planet', '-updated_at')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.String)
    nearest_star = db.Column(db.String)
    image = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    missions = db.relationship("Mission", backref="planet")

    def __repr__(self):
        return f'<Planet {self.id}: {self.name}>'

class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    serialize_rules = ('-missions.scientist', '-updated_at')

    @validates('name')
    def validate_name(self, name):
        if len(name) >= 1:
            return name
        else:
            raise ValueError('failed to validate name')
        
    @validates('field_of_study')
    def validate_field_of_study(self, key, field_of_study):
        if len(field_of_study) >= 1:
            return field_of_study
        else:
            raise ValueError('failed to validate field_of_study')
    

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    field_of_study = db.Column(db.String, nullable=False)
    avatar = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    missions = db.relationship("Mission", backref="scientist")

    

    def __repr__(self):
        return f'<Scientist {self.id}: {self.name}>'

class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'

    @validates('name')
    def validate_name(self, key, name):
        if len(name) >= 1:
            return name
        else:
            raise ValueError('failed to validate name')
        
    
    @validates('plant_id')
    def validate_planet_id(self, key, planet_id):
        if isinstance(planet_id, Planet.id):
            return planet_id
        else:
            raise ValueError('failed to validate planet_id')
    
        
    @validates('scientist_id')
    def validate_scientist_id(self,key, scientist_id):
        q = Mission.query.filter_by(id=scientist_id).all()
        q_names_list = [m.name for m in q]
        if isinstance(scientist_id, Scientist.id) and (q_names_list == set(q_names_list)):
            return scientist_id
        else:
            raise ValueError('failed to validate scientist_id')
        
    


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    scientist_id = db.Column(db.Integer,db.ForeignKey("scientists.id"))
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    serialize_rules = ('-planet.missions', '-scientist.missions', '-updated_at')

# add any models you may need. 