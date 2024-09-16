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

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    data = request.get_json()  

    user_id = data.get('user_id')

    user = User.query.get(user_id)
    planet = Planets.query.get(planet_id)

    if not user:
        return jsonify({"msg": "User doesn't exist"}), 404
    if not planet:
        return jsonify({"msg": "Planet not found or destroyed"}), 404

    
    existing_favorite = Favorites.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if existing_favorite:
        return jsonify({"msg": "You got this on favorite already"}), 400

    
    new_favorite = Favorites(user_id=user_id, planet_id=planet_id)

    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"msg": "Planet added to favorites"}), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):

    favorite = Favorites.query.filter_by(planet_id=planet_id).first()

    if favorite is None:
        return jsonify({"msg": "Favorite planet not found"}), 404

    
    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"msg": f"Planet with id {planet_id} has been eliminated from favorites by the Empire"}), 200


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

@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def add_favorite_character(character_id):
    data = request.get_json()  

    user_id = data.get('user_id')

    user = User.query.get(user_id)
    character = Characters.query.get(character_id)

    if not user:
        return jsonify({"msg": "User doesn't exist"}), 404
    if not character:
        return jsonify({"msg": "Character not found or be killed"}), 404

    
    existing_favorite = Favorites.query.filter_by(user_id=user_id, character_id=character_id).first()
    if existing_favorite:
        return jsonify({"msg": "You got this on favorite already"}), 400

    
    new_favorite = Favorites(user_id=user_id, character_id=character_id)

    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"msg": "Character added to favorites"}), 201

@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(character_id):

    favorite = Favorites.query.filter_by(character_id=character_id).first()

    if favorite is None:
        return jsonify({"msg": "Favorite character not found"}), 404

    
    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"msg": f"Character with id {character_id} has been eliminated by the Order 66"}), 200    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
