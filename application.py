import os

from flask import Flask, render_template, request, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *

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
engine = create_engine('postgresql://postgres:jono@localhost:5432/books')
db = scoped_session(sessionmaker(bind=engine))

#query = "select b.name as 'Book Name', b.description as 'Book Description', a.name as 'Author Name' from books as b join author as a on a.id = b.author_id;"

#books = db.execute("SELECT * from books").fetchall()  # execute this SQL command and return all of the results

@app.route("/", methods=["POST", "GET"])
def index():
    books = db.execute("SELECT * from books").fetchall()  # execute this SQL command and return all of the results

    if request.method == "POST":
        book = request.form.get("book") # match form var name
        #get variables from form
        #construct author object
        author = author.Author(name, age)
        #construct book object

        #add to database
        #commit to database
        #render template
    return render_template("index.html", books=books)


@app.route("/buy")
def buy():
    return render_template("buy.html")

# Routes - this must come before index route
@app.route("/<string:name>")
def hello(name):
    name = name
    return render_template("index.html", name=name)


@app.route('/Jono')
def Jono():
    return "Jono"

