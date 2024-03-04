from flask import Flask, render_template, url_for, request, redirect
from markupsafe import Markup
from flask_sqlalchemy import SQLAlchemy

import markdown
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///development.db'

settings = json.load(open("settings.json"))

db = SQLAlchemy(app)

@app.route("/")
def home():
    return render_template("home.html", wiki_name=settings["wiki-name"], wiki_logo=settings["wiki-logo"])

@app.route("/article")
def article(id="test"):
    body = markdown.markdown(open("test.md", "r", encoding='utf8').read())
    return render_template("article.html", wiki_name=settings["wiki-name"], wiki_logo=settings["wiki-logo"], body=Markup(body))

@app.route("/create-article", methods=["GET", "POST"])
def create_article():
    return "Create Article Page"

@app.route("/update-article", methods=["GET", "POST"])
def update_article():
    return "Update Article Page"

@app.route("/delete-article", methods=["POST"])
def delete_article():
    return "Delete Article Page"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)