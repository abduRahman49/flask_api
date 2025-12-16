import json
from flask import Flask, render_template, request, jsonify, abort
from models import db, User, Tache
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

# Schéma d'entrée : Données des taches
class TacheInSchema(ma.Schema):
    libelle = fields.Str(required=True)
    description = fields.Str(required=True)
    etat = fields.Str(required=True)


# Schéma de sortie : Représentation de la ressource utilisateur
class TacheOutSchema(ma.Schema):
    id = fields.Int()
    libelle = fields.Str()
    description = fields.Str()


class ListeTachesOutSchema(ma.Schema):
    id = fields.Int()
    libelle = fields.Str()
    description = fields.Str()


class UserOutSchema(ma.Schema):
    id = fields.Int()
    nom = fields.Str()
    prenom = fields.Str()
    email = fields.Email()
    taches = fields.Nested(TacheOutSchema, many=True)
    listes_taches = fields.Nested(ListeTachesOutSchema, many=True)


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


@app.route('/users', methods=["GET"])
def list_users():
    liste_utilisateurs = db.session.execute(db.select(User).order_by(User.nom.desc())).scalars().all()
    user_out_schema = UserOutSchema(many=True)
    return user_out_schema.dump(liste_utilisateurs), 200


@app.route('/users/<int:id>', methods=["GET"])
def get_user(id):
    # traitement pour récupérer un seul élément à partir de son id
    user = db.session.execute(db.select(User).where(User.id == id)).scalar_one_or_none()
    if user is None:
        return jsonify({"message": "User does not exist"}), 404
    user_out_schema = UserOutSchema()
    return user_out_schema.dump(user), 200

@app.route('/users/<int:id>/taches', methods=["POST"])
def create_tache_user(id):

    data = request.json
    tache_in_schema = TacheInSchema()
    try:
        validated_data = tache_in_schema.load(data)
    except ValidationError as e:
        return jsonify({"message": e.messages}), 400
    
    user = db.session.execute(db.select(User).where(User.id==id)).scalar_one_or_none()
    if user is None:
        return jsonify({"message": "User does not exist"}), 404
    
    tache = Tache(**validated_data)
    db.session.add(tache)
    db.session.commit()

    user.taches.append(tache)
    db.session.commit()
    tache_out_schema = TacheOutSchema()
    return tache_out_schema.dump(tache), 201


@app.route('/taches', methods=["GET"])
def liste_taches():
    etat = request.args.get("etat")
    user_id = request.args.get("user_id")

    return jsonify({"etat": etat, "user_id": user_id}), 200



# elle vérifie si l'application est lancée en tant que module / script
if __name__ == '__main__':
    app.run("0.0.0.0", 5000, debug=True)
