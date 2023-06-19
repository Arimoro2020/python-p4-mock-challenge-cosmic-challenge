from random import randint, choice as rc

from faker import Faker

from app import app
from models import db, Planet, Scientist, Mission

fake = Faker()

if __name__ == '__main__':

    with app.app_context():
        print("Clearing db...")
        Planet.query.delete()
        Scientist.query.delete()
        Mission.query.delete()

        scientists = []
        for i in range(100):
            u = Scientist(name=fake.name(),field_of_study=fake.name(), avatar=fake.url())
            scientists.append(u)  

        db.session.add_all(scientists)
        db.session.commit()

        planets = []
        for i in range(100):
            u = Planet(name=fake.name(),distance_from_earth=randint(1000, 20000000), nearest_star=fake.name(), image=fake.url())
            planets.append(u)

        db.session.add_all(planets)
        db.session.commit()

        missions = []
        for i in range(100):
            u = Mission(name=fake.name(), scientist_id= randint(1, 101), planet_id=randint(1, 101))
            missions.append(u)

        db.session.add_all(missions)
        db.session.commit()

        
        print("Done seeding!")
