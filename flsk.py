from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "mamahuevo"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes = 3)

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))

    def __init__(self, name, email):
        self.name = name
        self.email = email



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/view")
def view():
    return render_template("view.html", values = users.query.all())

@app.route("/test")
def test():
    return render_template("tets.html")

@app.route("/log", methods = ["POST", "GET"])
def log():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        user_exist = users.query.filter_by(name = user).first()
        if user_exist:
            session["email"] = user_exist.email
        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()

        flash("Log succes")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Ya estas")
            return redirect(url_for("user"))
        return render_template("log.html")
    

@app.route("/user", methods = ["POST", "GET"])
def user():
    email = None
    if "user" in  session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            user_exist = users.query.filter_by(name = user).first()
            user_exist.email = email
            db.session.commit()
            flash("Guardado")
        else:
            if "email" in  session:
                email = session["email"]
        return render_template("user.html", email = email)
    else:
        flash("todavia no estas")
        redirect(url_for("log"))

@app.route("/out")
def out():
    if "user" in  session:
        user = session["user"]
        flash(f"ya te fuiste, {user}", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("log"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug = True)