from flask import Flask, render_template, url_for, request, redirect
from markupsafe import Markup
from flask_sqlalchemy import SQLAlchemy

import markdown
import json

app = Flask(__name__)
app.config['SQL_ALCHEMY_DATABASE_URI'] = f'sqlite:///development.db'

settings = json.load(open("settings.json"))

db = SQLAlchemy(app)

@app.route("/")
def home():
    return render_template("base.html", wiki_name=settings["wiki-name"], wiki_logo=settings["wiki-logo"])

@app.route("/create-article")
def create_article():
    return "Create Article Page"

@app.route("/update-article")
def update_article():
    return "Update Article Page"

@app.route("/delete-article")
def delete_article():
    return "Delete Article Page"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)