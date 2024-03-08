from flask import Flask, render_template, url_for, request, redirect, flash
from markupsafe import Markup
from flask_sqlalchemy import SQLAlchemy
import markdown
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///development.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "dev"

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

# Flask routes

@app.route("/", methods=["GET"])
def home():
    articles = Article.query.all()
    return render_template("home.html", articles=articles, wiki_name=settings["wiki-name"], wiki_logo=settings["wiki-logo"])

@app.route("/article", methods=["GET"])
def article():
    print("ROUTED")
    id = request.args.get("id")
    article = Article.query.filter(Article.id == id).first()
    content = Markup(markdown.markdown(article.content))
    return render_template("article.html", article_name=article.name, article_content=content, wiki_name=settings["wiki-name"], wiki_logo=settings["wiki-logo"])

@app.route("/create-article", methods=["GET", "POST"])
def create_article():
    if request.method == "POST":
        print(request.form) # testing code
        article = Article(name=request.form["name"], content=request.form["content"])
        db.session.add(article)
        db.session.commit()
        flash("Article Successfully Created!")
        return redirect(url_for("home"))
    else:
        return render_template("create_article.html", wiki_name=settings["wiki-name"], wiki_logo=settings["wiki-logo"])

@app.route("/update-article", methods=["GET", "POST"])
def update_article():
    if request.method == "POST":
        id = request.form["id"]
        article = Article.query.filter(Article.id == id).first()
        article.name = request.form["name"]
        article.content = request.form["content"]
        db.session.commit()
        flash("Article Successfully Updated!")
        return redirect(url_for("update_article", id=id))
    else:
        id = request.args.get("id")
        article = Article.query.filter(Article.id == id).first()
        return render_template("update_article.html", id=id, article_name=article.name, article_content=article.content, wiki_name=settings["wiki-name"], wiki_logo=settings["wiki-logo"])

@app.route("/delete-article", methods=["GET"])
def delete_article():
    id = request.args.get("id")
    article = Article.query.filter(Article.id == id).first()
    if article is not None:
        db.session.delete(article)
        db.session.commit()
        flash("Article Successfully Deleted!")
    return redirect(url_for("home"))

@app.route("/generate-preview", methods=["POST"])
def generate_preview():
    body = request.form["Content"]
    print(body)
    content = Markup(markdown.markdown(body))
    return content

# Mainloop

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)