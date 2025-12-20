from flask import Blueprint, request, jsonify


taches_bp = Blueprint('taches', __name__)


@taches_bp.route('/taches', methods=["GET"])
def liste_taches():
    etat = request.args.get("etat")
    user_id = request.args.get("user_id")

    return jsonify({"etat": etat, "user_id": user_id}), 200