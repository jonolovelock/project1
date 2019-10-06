# Project 1

Web Programming with Python and JavaScript

## How to initialize the app ##
1. Create a postgres DB, either locally or externally hosted (for Harvard Web Dev, set up on Heroku
your external DB, and set your environment variables 
as explained in Project 1 Instructions: https://docs.cs50.net/web/2019/x/projects/1/project1.html)

2. Connect to the Heroku CLI (explained in Heroku set up), this will connect you to the default database
created for you by Heroku. Then open sql/bookDDL.sql, copy paste the Data Definition Language to
Create tables for Books, Users, Reviews against your Heroku DB (you can validate this was successful
by checking the Heroku dasboard)

3. Navigate to your project directory on the command line and run import.py to load your heroku DB, 
this may take a few minutes. If any connection issues, confirm your environment set up is as specified 
in step 1.
 
4. You are now ready to run this flask app

## Files ##

application.py
Includes all program logic to:
- import all necessary modules
- establish database connection
- expose routes accessible over HTTP, that will return either a HTML page or an API response

books.csv
- initial seed data for the application database
import.py
- contain the logic needed to load books.csv to a database of your choice (specified via DATABASE_URL)

sql/boolDDL.SQL

templates/layout
- Parent HTML template including navbar, stylesheet and script tags that are inherited by all child templates
templates/index
- The index page for this app

templates/register
- The page for users to register an account

templates/login
- The page for registered users to log in

templates/books
- The page for users to search for a book against our book database (seeded by books.csv)

templates/book
- The detailed book page where users can see complete details for a book, read reviews left by other, 
leave their own reviews and read data pulled in from Goodreads.com via API
