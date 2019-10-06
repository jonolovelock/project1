import os
import requests

from flask import Flask, render_template, request, session, jsonify
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
engine = create_engine(os.getenv("DATABASE_URL"))
#engine = create_engine('postgresql://postgres:jono@localhost:5432/bookshop')
db = scoped_session(sessionmaker(bind=engine))


@app.route("/books", methods=["GET", "POST"])
def books():
    if request.method == "POST":
        if request.form.get("isbn"):
            formIsbn = "%" + request.form.get("isbn") + "%"
            if db.execute("SELECT * from books WHERE isbn LIKE :isbn", {"isbn": formIsbn}).rowcount == 0:
                return render_template("error.html", message="No books where found.")
            books = db.execute("SELECT * from books WHERE isbn LIKE :isbn", {"isbn": formIsbn})

        if request.form.get("title"):
            formTitle = "%" + request.form.get("title") + "%"
            if db.execute("SELECT * from books WHERE title LIKE :title", {"title": formTitle}).rowcount == 0:
                return render_template("error.html", message="No books where found.")
            books = db.execute("SELECT * from books WHERE title LIKE :title", {"title": formTitle})

        if request.form.get("author"):
            formAuthor = "%" + request.form.get("author") + "%"
            if db.execute("SELECT * from books WHERE author LIKE :author", {"author": formAuthor}).rowcount == 0:
                return render_template("error.html", message="No books where found.")
            books = db.execute("SELECT * from books WHERE author LIKE :author", {"author": formAuthor})
        return render_template("books.html", books=books)
    return render_template("books.html")


@app.route("/books/<int:book_id>", methods=["GET", "POST"])
def book(book_id):
    if request.method == "POST":
        rating = request.form.get("rating")
        newReview = request.form.get("textreview")

        currentUser = session["user_id"]
        reviewList = db.execute("SELECT reviewer, book from reviews WHERE reviewer = :reviewer", {"reviewer": currentUser})
        for review in reviewList:
            if review.reviewer == currentUser and review.book == book_id:
                return render_template("error.html", message="Sorry, you are only able to submit one review per book")

        db.execute("INSERT into reviews"
                   "(rating, review, reviewer, book)"
                   "VALUES (:rating, :review, :reviewer, :book_id)",
                   {"rating": rating,
                    "review": newReview,
                    "reviewer": currentUser,
                    "book_id": book_id})
        db.commit()

    dbbook = db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id})

    dbreviews = db.execute("SELECT rev.rating as rating, rev.review as review, "
                           "concat_ws(' ', users.firstname, users.lastname) as reviewer "
                           "FROM reviews rev Left Join users on rev.reviewer = users.id WHERE rev.book = :id",
                           {"id": book_id})
    for newBook in dbbook:
        res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": "OtyNZazIiejX4HFNpx80cA", "isbns": newBook.isbn})
        if res.status_code == 200:
            goodReads = res.json()
            print(goodReads)
            grCount = goodReads['books'][0]['work_ratings_count']
            grRating = goodReads['books'][0]['average_rating']
            print(grCount)
            print(grRating)
            return render_template("book.html", book=newBook, reviews=dbreviews, grCount=grCount, grRating=grRating)
        else:
            return render_template("book.html", book=newBook, reviews=dbreviews)

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
                session["user_id"] = user.id
                message = "You have successfully logged in"
            else:
                message = "Incorrect User Name or Password"
            return render_template("index.html", message=message)
    return render_template("login.html")

@app.route("/api/<string:isbn>")
def books_api(isbn):
    if db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).rowcount == 0:
        return jsonify({"error": "There are no books with that ISBN"}), 404
    dbBook = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn})
    for book in dbBook:
        #title = book.title
        #author = book.author
        #year = book.year
        #isbn = book.isbn

        review_count = 99
        db_review_count = db.execute("SELECT COUNT(*) as count FROM reviews where book = :book", {"book": book.id})
        for review in db_review_count:
            review_count = str(review.count)

        ave_score = 99
        db_ave_score = db.execute("SELECT AVG(rating) as ave FROM reviews where book = :book", {"book": book.id})
        for score in db_ave_score:
            if score.ave:
                ave_score = str(round(score.ave, 1))
            else:
                ave_score = 0
        return jsonify({
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "isbn": book.isbn,
            "review_count": review_count,
            "average_score": ave_score
        })

@app.route("/logout")
def logout():
    session.clear()
    return render_template("index.html")

@app.route("/")
def index():
    return render_template("index.html")
