from flask_sqlalchemy import SQLAlchemy

  db = SQLAlchemy()

  class Author(db.Model):
      __tablename__ = "author"
      id = db.Column(db.Integer, primary_key=True)
      name = db.Column(db.String, nullable=False)
      age = db.Column(db.age, nullable=True)


  class Book(db.Model):
      __tablename__ = "passengers"
      id = db.Column(db.Integer, primary_key=True)
      title = db.Column(db.String, nullable=False)
      description = db.Column(db.String, nullable=False)
      author_id = db.Column(db.Integer, db.ForeignKey("author.id"), nullable=False)