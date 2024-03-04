from flask import Flask, render_template, url_for, request, redirect
from markupsafe import Markup
from flask_sqlalchemy import SQLAlchemy
from models import Article
import markdown
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///development.db'

settings = json.load(open("settings.json"))

db = SQLAlchemy(app)

# Models

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True) # auto assigns names in db
    name = db.Column(db.Text)
    content = db.Column(db.Text)

    def __init__(self, name, content):
        self.name = name
        self.content = content


@app.route("/")
def home():
    articles = Article.query
    print(articles)
    return render_template("home.html", wiki_name=settings["wiki-name"], wiki_logo=settings["wiki-logo"])

@app.route("/article")
def article(id="test"):
    body = markdown.markdown(open("test.md", "r", encoding='utf8').read())
    return render_template("article.html", wiki_name=settings["wiki-name"], wiki_logo=settings["wiki-logo"], body=Markup(body))

@app.route("/create-article", methods=["GET", "POST"])
def create_article():
    if request.method == "POST":
        print(request.form) # testing code
        article = Article(name=request.form["name"], content=request.form["content"])
        db.session.add(article)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        return render_template("create_article.html")

@app.route("/update-article", methods=["GET", "POST"])
def update_article():
    return "Update Article Page"

@app.route("/delete-article", methods=["POST"])
def delete_article():
    return "Delete Article Page"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)