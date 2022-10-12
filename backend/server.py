"""Server for medication tracker app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db, User, Medication
from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "takeyourbestshot22594"
app.jinja_env.undefined = StrictUndefined



@app.route("/", methods=["GET", "POST"])
def homepage():
    """View homepage."""

    return "Hello, from Flask!"

#USERS

@app.route("/users", methods=["GET", "POST"])
def register_user():
    """Create a new user."""

    if request.method == "POST":
        
        email = request.form.get("email")
        password = request.form.get("password")
            
        user = User.get_by_email(email)

        if user:
            flash("An account with this email already exists. Try again.")

        else:
            user = User.create(email, password)
            db.session.add(user)
            db.session.commit()
            flash("Account created! Please log in.")

    return redirect("/")


@app.route("/users/my-profile")
def my_profile():
    """Show details on a particular user."""

    if "user_email" in session:
        user = User.get_by_email(session["user_email"])
    else:
        flash("Please log in!")
        return redirect("/")

    return render_template("user-details.html", user=user)


@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.get_by_email(email)

    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
        return redirect('/')

    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        user = User.get_by_email(session["user_email"])

        return render_template("user-details.html", user=user)


@app.route('/logout')
def logout():
    session.pop('user_email', None)
    return redirect('/')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0")