from flask_marshmallow import Marshmallow
from marshmallow.exceptions import ValidationError
from marshmallow import fields


ma = Marshmallow()

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

