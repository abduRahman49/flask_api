from flask import Blueprint, request, jsonify, abort
from extensions.models import db, User, Tache
from extensions.schemas import UserInSchema, UserOutSchema, TacheInSchema, TacheOutSchema
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError, NoResultFound


users_bp = Blueprint('users', __name__)

# Endpoint permettant de créer un utilisateur
@users_bp.route('/users', methods=['POST'])
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


@users_bp.route('/users', methods=["GET"])
def list_users():
    liste_utilisateurs = db.session.execute(db.select(User).order_by(User.nom.desc())).scalars().all()
    user_out_schema = UserOutSchema(many=True)
    return user_out_schema.dump(liste_utilisateurs), 200


@users_bp.route('/users/<int:id>', methods=["GET"])
def get_user(id):
    # traitement pour récupérer un seul élément à partir de son id
    # user = db.session.execute(db.select(User).where(User.id == id)).scalar_one_or_none()
    # if user is None:
    #     return jsonify({"message": "User does not exist"}), 404
    try:
        user = db.session.get_one(User, id)
    except NoResultFound:
        raise abort(404, description="User does not exist")

    user_out_schema = UserOutSchema()
    return user_out_schema.dump(user), 200

@users_bp.route('/users/<int:id>/taches', methods=["POST"])
def create_tache_user(id):

    data = request.json
    tache_in_schema = TacheInSchema()
    try:
        validated_data = tache_in_schema.load(data)
    except ValidationError as e:
        return jsonify({"message": e.messages}), 400
    
    try:
        user = db.session.get_one(User, id)
    except NoResultFound:
        raise abort(404, description="User does not exist")
    # user = db.session.execute(db.select(User).where(User.id==id)).scalar_one_or_none()
    # if user is None:
    #     return jsonify({"message": "User does not exist"}), 404
    
    tache = Tache(**validated_data)
    db.session.add(tache)
    db.session.commit()

    user.taches.append(tache)
    db.session.commit()
    tache_out_schema = TacheOutSchema()
    return tache_out_schema.dump(tache), 201