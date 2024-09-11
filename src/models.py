from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    subscription = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    lastname = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "subscription":self.subscription,
            "name":self.name,
            "lastname": self.lastname
            # do not serialize the password, its a security breach
        }

# class Planets(db.Model):
#     __tablename__ = 'planet'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(250), nullable=False)
#     population = db.Column(db.String(250), nullable=False)
#     location = db.Column(db.String(250), nullable=False)

#     def __repr__(self):
#         return '<Planets %r>' % self.name

#     def serialize(self):
#         return {
#             "id": self.id,
#             "name":self.name,
#             "population": self.population,
#             "location": self.location
#             # do not serialize the password, its a security breach
#         }

# class Characters(db.Model):
#     __tablename__ = 'character'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(250), nullable=False)
#     height = db.Column(db.String(250), nullable=False)
#     gender = db.Column(db.String(250), nullable=False)
#     eye_color = db.Column(db.String(250), nullable=False)

#     def __repr__(self):
#         return '<Characters %r>' % self.name

#     def serialize(self):
#         return {
#             "id": self.id,
#             "height": self.height,
#             "gender":self.gender,
#             "name":self.name,
#             "eye_color": self.eye_color
#             # do not serialize the password, its a security breach
#         }

# class Favorites(db.Model):
#     __tablename__ = 'favorite'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
#     character_id = db.Column(db.Integer, db.ForeignKey('character.id'))