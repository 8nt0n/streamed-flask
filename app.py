import os

import subprocess
import sys
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, make_response, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["MAX_CONTENT_LENGTH"] = 200 * 1024 * 1024 * 1024 # kaplau... kaboom max upload file size is now 200GB
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///streamed.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# --------------------------index--------------------------#

@app.route("/")
@login_required
def index():

    if request.method == "POST":
        return apology("TODO")
    else:
        return render_template("index.html")


# --------------------------login--------------------------#

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]

        # can assume the forms username is correct because we queried the db with it right?
        session["user_name"] = request.form.get("username")

        return redirect("/")
    else:
        return render_template("login.html")


# --------------------------logout--------------------------#

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# --------------------------register--------------------------#

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # just some shit that could go wrong (if the user has like... potatoe iq)
        if not request.form.get("username"):
            return apology("must provide username", 400)

        if not request.form.get("password"):
            return apology("must provide password", 400)

        if not request.form.get("confirmation"):
            return apology("must provide password confirmation", 400)

        if request.form.get("confirmation") != request.form.get("password"):
            return apology("passwords dont match", 400)

        # Insert into db
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?);", request.form.get(
                "username"), generate_password_hash(request.form.get("password")))
        except ValueError:
            return apology("User already exists", 400)

        return redirect("/")

    else:
        return render_template("register.html")
    

# --------------------------dashboard--------------------------#

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    if request.method == "GET":
        return render_template("dashboard.html", name=session["user_name"])
    else:
        return apology("w345rtzg")



# ------------------------upload movie------------------------#

@app.route("/upload_movie", methods=["GET", "POST"]) 
def upload_movie():
    if request.method == "GET":
        return render_template("upload_movie.html")
    
    if request.method == "POST":
        movie_name = secure_filename(request.form.get("moviename")) # this makes sure bad people cant come into the code :)
        description = request.form.get("description")
        movie_file = request.files.get("movie_file")
        poster_file = request.files.get("poster_file")


        # like check if eversthing has been typed in
        if not movie_name:
            return apology("missing movie name", 400)

        if not description:
            return apology("missing description", 400)

        if not movie_file:
            return apology("missing movie file", 400)

        if not poster_file:
            return apology("missing poster image", 400)
        
        # check for right fileformat 
        if not movie_file.filename.endswith(".mp4"):
            return apology("movie must be mp4", 400)
        
        if not poster_file.filename.endswith(".png"):
            return apology("poster must be png", 400)


        # try to create a folder or if the user is stupid dont (no its fine we all forget how our movies are named)
        try:
            os.makedirs(f"static/media/movies/{movie_name}/meta", exist_ok=False) 
        except FileExistsError:
            return apology("movie already exists")
        
        # write the description for the movie into description.txt
        with open(f"static/media/movies/{movie_name}/meta/description.txt", "w") as descriptionFile:
            descriptionFile.write(description)

        # save the video and img
        movie_file.save(f"static/media/movies/{movie_name}/{movie_name}.mp4")
        poster_file.save(f"static/media/movies/{movie_name}/meta/thumbnail.png")

        # run refresh.py (man tbh i dont know if thats the clean way to do this, desperate times ok?)
        script_path = "static/_tools/refresh.py"
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True
        )

        print(result)        

        return redirect("/")
    



# ------------------------upload series------------------------#

@app.route("/upload_series", methods=["GET", "POST"]) 
def upload_series():
    if request.method == "GET":
        return render_template("upload_series.html")
    
    if request.method == "POST":
        # Get master series info
        series_title = secure_filename(request.form.get("series_title")) # making sure bad people can't do bad things
        description = request.form.get("series_description")
        series_cover = request.files.get("series_cover")

        # Validate master series info
        if not series_title:
            return apology("missing series title", 400)
        if not description:
            return apology("missing series description", 400)
        if not series_cover:
            return apology("missing main series cover", 400)
        if not series_cover.filename.endswith(".png"):
            return apology("series cover must be png", 400)

        # Set up base paths
        base_path = f"static/media/series/{series_title}"
        meta_path = f"{base_path}/meta"

        # Try to create the series and meta folders
        try:
            os.makedirs(meta_path, exist_ok=False)
        except FileExistsError:
            return apology("series already exists", 400)
        with open(f"{meta_path}/description.txt", "w") as descriptionFile:
            descriptionFile.write(description)
        series_cover.save(f"{meta_path}/0.png")

        # Get the maximum number of seasons added in the form
        try:
            max_season_index = int(request.form.get("max_season_index", 1))
        except ValueError:
            max_season_index = 1

        for i in range(1, max_season_index + 1):
            cover_field = f"season_{i}_cover"
            episodes_field = f"season_{i}_episodes"

            # Check if this specific season was actually uploaded
            if cover_field in request.files:
                season_cover = request.files.get(cover_field)
                season_episodes = request.files.getlist(episodes_field) # getlist handles multiple file uploads

                # Validation for the season files
                if not season_cover or not season_cover.filename.endswith(".png"):
                    return apology(f"season {i} cover missing or not png", 400)
                
                if not season_episodes or all(ep.filename == '' for ep in season_episodes):
                    return apology(f"season {i} is missing episodes", 400)

                season_cover.save(f"{meta_path}/{i}.png")
                season_path = f"{base_path}/{i}"
                os.makedirs(season_path, exist_ok=True)

                for episode in season_episodes:
                    if episode and episode.filename:
                        if not episode.filename.endswith(".mp4"):
                            return apology(f"season {i} episodes must be mp4", 400)
                        
                        safe_ep_name = secure_filename(episode.filename)
                        episode.save(f"{season_path}/{safe_ep_name}")

        # Run refresh.py
        script_path = "static/_tools/refresh.py"
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True
        )

        print(result)        

        return redirect("/")