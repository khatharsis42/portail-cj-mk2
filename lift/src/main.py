from flask import Flask, render_template
from src.minecraft import mc

app = Flask(__name__, template_folder="../templates", static_folder="../static")

app.register_blueprint(mc)

@app.route("/")
def index():
    return render_template("accueil.html")
