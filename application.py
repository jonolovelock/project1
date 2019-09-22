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
# engine = create_engine(os.getenv("DATABASE_URL"))
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


@app.route("/books/<int:book_id>", methods=["GET", "POST"])
def book(book_id):
    if request.method == "POST":
        rating = request.form.get("rating")
        review = request.form.get("review")
        reviewer = request.form.get("reviewer")
        db.execute("INSERT into reviews"
                   "(rating, review, reviewer, book)"
                   "VALUES (:rating, :review,:reviewer, :book_id)",
                   {"rating": rating,
                    "review": review,
                    "reviewer": reviewer,
                    "book_id": book_id})
        db.commit()

    # Although only one book, flask still treats SQL response as a list
    dbbook = db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id})

    #probably inefficent to connext to DB twice
    dbreviews = db.execute("SELECT * FROM reviews WHERE book = :id", {"id": book_id})

    return render_template("book.html", books=dbbook, reviews=dbreviews)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        password = request.form.get("password")
        db.execute("INSERT into users"
                   "(username, firstname, lastname, email, password)"
                   "VALUES(:username, :firstname, :lastname, :email, :password)",
                   {"username": username,
                    "firstname": firstname,
                    "lastname": lastname,
                    "email": email,
                    "password": password})
        newuser = db.execute("select currval('users_id_seq')")
        newID = 0
        for user in newuser:
            newID = user.currval
        user = db.execute("Select * from users where id = :id", {"id": newID})
        db.commit()
        return render_template("register.html", users=user)
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        dbuser = db.execute("Select * from users where username= :username", {"username": username})
        for user in dbuser:
            if user.password == password:
                session["user_id"]= user.id
                print(session["user_id"])
                message = "You have successfully loggged in"
            else:
                message = "Incorrect User Name or Password"
            return render_template("login.html", message=message)
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return render_template("index.html")

@app.route("/")
def index():
    return render_template("index.html")
