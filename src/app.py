"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, Characters, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()  
    response_body = [user.serialize() for user in users]  
    return jsonify(response_body)

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "user not found"}), 404
    return jsonify(user.serialize())

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    favorites = Favorites.query.filter_by(user_id=user_id).all()
    response_body = []
    
    for favorite in favorites:
        favorite_data = {
            "id": favorite.id,
            "user_id": favorite.user_id,
            "planet_id": favorite.planet_id,
            "character_id": favorite.character_id
        }
        response_body.append(favorite_data)
    
    return jsonify(response_body)

# @app.route('/user', methods=['POST'])
# def create_users():
#     data = request.json
#     new_user = User(
#         name=data['name'],
#         lastname=data['lastname'],
#         username=data['username'],
#         email=data['email'],
#         password=data['password'],
#         is_active=data.get('is_active', True) 
#     )
#     db.session.add(new_user)
#     db.session.commit()
#     return jsonify(new_user.serialize()), 201

@app.route('/planet', methods=['GET'])
def get_planets():
    planets = Planets.query.all()  
    response_body = [planet.serialize() for planet in planets]  
    return jsonify(response_body)

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify(planet.serialize())


# @app.route('/planet', methods=['POST'])
# def create_planets():
#     data = request.json
#     new_planet = Planets(
#         name=data['name'],
#         population=data['population'],
#         location=data['location'],
#     )
#     db.session.add(new_planet)
#     db.session.commit()
#     return jsonify(new_planet.serialize()), 201

@app.route('/character', methods=['GET'])
def get_characters():
    characters = Characters.query.all()  
    response_body = [character.serialize() for character in characters]  
    return jsonify(response_body)

@app.route('/character/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Characters.query.get(character_id)
    if character is None:
        return jsonify({"error": "Character doesn't exist"}), 404
    return jsonify(character.serialize())

# @app.route('/character', methods=['POST'])
# def create_characters():
#     data = request.json
#     new_character = Characters(
#         name=data['name'],
#         height=data['height'],
#         gender=data['gender'],
#         eye_color=data['eye_color'],
#     )
#     db.session.add(new_character)
#     db.session.commit()
#     return jsonify(new_character.serialize()), 201

    
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
