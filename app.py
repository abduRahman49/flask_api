import json
from flask import Flask, render_template
from models import db


# création de l'application depuis la classe Flask
app = Flask(__name__)
app.config.from_file('./config.json', load=json.load)
db.init_app(app)

# définition de la route de base /
@app.route("/")
def index():
    return render_template("index.html")

# elle vérifie si l'application est lancée en tant que module / script
if __name__ == '__main__':
    app.run("0.0.0.0", 5000, debug=True)
