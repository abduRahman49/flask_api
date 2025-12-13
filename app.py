import json
from flask import Flask, render_template, request, jsonify
from models import db, User
from migrations import migrate
from schemas import ma
# erreurs de validation (données client)
from marshmallow.exceptions import ValidationError
# erreur base de données (contrainte d'intégrité)
from sqlalchemy.exc import IntegrityError
from marshmallow import fields


# création de l'application depuis la classe Flask
app = Flask(__name__)
app.config.from_file('./config.json', load=json.load)
# initialisation des extensions
db.init_app(app)
migrate.init_app(app, db)
ma.init_app(app)


def is_isi_email(value: str):
    if not value.endswith("@isi.com"):
        raise ValidationError("Cette adresse n'est pas une adresse de ISI")

# Schéma d'entrée : Données utilisateur
class UserInSchema(ma.Schema):
    nom = fields.Str(required=True)
    prenom = fields.Str(required=True)
    email = fields.Email(required=True, validate=is_isi_email)
    password = fields.Str(required=True)


# Schéma de sortie : Représentation de la ressource utilisateur
class UserOutSchema(ma.Schema):
    id = fields.Int()
    nom = fields.Str()
    prenom = fields.Str()
    email = fields.Email()


# définition de la route de base /
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/contact")
def contact():
    return "Ceci est ma page de contact"

# Endpoint permettant de créer un utilisateur
@app.route('/users', methods=['POST'])
def create_user():
    # récupère les informations de l'utilisateur
    data = request.json

    # initialisation du schéma d'entrée (pour validation)
    user_in_schema = UserInSchema()
    # vérification des données par rapport aux contraintes définies sur le schéma
    try:
        validated_data = user_in_schema.load(data)
    except ValidationError as e:
        return jsonify({"erreur": f"L'erreur suivante s'est produite {e}"}), 400
    
    # création de l'objet
    user = User(**validated_data)
    # persistance de l'objet en base
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        return jsonify({"erreur": f"Ce compte existe déjà"}), 409

    # initialisation du schéma de sortie (pour représentation)
    user_out_schema = UserOutSchema()
    return user_out_schema.dump(user), 201


# elle vérifie si l'application est lancée en tant que module / script
if __name__ == '__main__':
    app.run("0.0.0.0", 5000, debug=True)
