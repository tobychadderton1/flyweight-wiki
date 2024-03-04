from server import db

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True) # auto assigns names in db
    name = db.Column(db.Text)
    content = db.Column(db.Text)

    def __init__(self, name, content):
        self.name = name
        self.content = content