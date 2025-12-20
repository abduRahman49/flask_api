import json
from flask import Flask, render_template, jsonify
from models import db
from migrations import migrate
from schemas import ma
from routes.users import users_bp
from routes.taches import taches_bp


# création de l'application depuis la classe Flask
app = Flask(__name__)
app.config.from_file('./config.json', load=json.load)
# enregistrement des blueprints et disponibilité des routes associées à la ressource User
app.register_blueprint(users_bp)
app.register_blueprint(taches_bp)
# initialisation des extensions
db.init_app(app)
migrate.init_app(app, db)
ma.init_app(app)


# définition de la route de base /
@app.route("/")
def index():
    return render_template("index.html")


# Gestion d'exceptions
# ressource non trouvée
@app.errorhandler(404)
def not_found_handler(error):
    return jsonify({
        "status": 404,
        "message": str(error)
    }), 404

# erreur serveur
@app.errorhandler(500)
def internal_error_handler(error):
    return jsonify({
        "status": 500,
        "message": str(error)
    }), 500

# service indisponible
@app.errorhandler(503)
def internal_error_handler(error):
    return jsonify({
        "status": 503,
        "message": str(error)
    }), 503


# elle vérifie si l'application est lancée en tant que module / script
if __name__ == '__main__':
    app.run("0.0.0.0", 5000, debug=True)
