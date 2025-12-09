import json
from flask import Flask, render_template, request
from models import db, Tache
from migrations import migrate
from schemas import ma
from marshmallow.exceptions import ValidationError
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

@app.route("/users/<int:user_id>")
def display_user(user_id):
    return f"Ceci est l'identifiant de l'utilisateur {user_id}"

@app.route('/taches', methods=["GET", "POST"])
def tasks():
    if request.method == "GET":
        # traitement pour récupérer toutes les taches
        taches = db.session.execute(db.select(Tache)).scalars().all()
    
    if request.method == "POST":
        # traitement pour créer une nouvelle tâche
        pass


# elle vérifie si l'application est lancée en tant que module / script
if __name__ == '__main__':
    app.run("0.0.0.0", 5000, debug=True)
