import os

from flask import Flask, render_template, request, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
# temp config
app.config["FLASK_DEBUG"] = True

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

# Set up database
#engine = create_engine(os.getenv("DATABASE_URL"))
engine = create_engine('postgresql://postgres:jono@localhost:5432/bookshop')
db = scoped_session(sessionmaker(bind=engine))


@app.route("/books", methods=["GET", "POST"])
def books():
    if request.method == "POST":
        if request.form.get("isbn"):
            formIsbn = "%" + request.form.get("isbn") + "%"

            books = db.execute("SELECT * from books WHERE isbn LIKE :isbn", {"isbn": formIsbn})
        if request.form.get("title"):
            formTitle = "%" + request.form.get("title") + "%"

            books = db.execute("SELECT * from books WHERE title LIKE :title", {"title": formTitle})
        if request.form.get("author"):
            formAuthor = "%" + request.form.get("author") + "%"

            books = db.execute("SELECT * from books WHERE author LIKE :author", {"author": formAuthor})
        return render_template("books.html", books=books)
    return render_template("books.html")

@app.route("/book/:id", methods=["GET", "POST"])
def book():
    if request.method == "POST":
        pass
        #add a book review
    #go to database with id and get book object
    #pass book object to book page
    return render_template("book.html")

@app.route("/register")
def register():
    return  render_template("register.html")


@app.route("/login")
def login():
    return  render_template("register.html")


@app.route("/")
def index():
    #books = db.execute("SELECT * from books").fetchall()  # execute this SQL command and return all of the results
    return render_template("index.html")
