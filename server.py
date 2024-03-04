from flask import Flask, render_template, url_for, request
from markupsafe import Markup

import markdown
import json

app = Flask(__name__)
settings = json.load(open("settings.json"))

@app.route("/")
def home():
    return render_template("base.html", wiki_name=settings["wiki-name"], wiki_logo=settings["wiki-logo"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)