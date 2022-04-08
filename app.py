
from flask import Flask, render_template, request, session, redirect, url_for

import datetime 


# FlASK
#############################################################
app = Flask(__name__)

#Generar sesión de un año
app.permanent_session_lifetime = datetime.timedelta(days=365)
app.secret_key = "super secret key"

#############################################################

@app.route('/')
def home():
    email = None


    if "email" in session:
        email = session["email"]
        return render_template('index.html', error = email)
    else:
        return render_template('login.html', error = email)


@app.route('/login', methods = ["GET", "POST"])
def login():
    email = None
    if "email" in session:
        return render_template("index.html", error = email)
    else:

        if(request.method == "GET"):
            return render_template("login.html", error= email)
        else:
            email = request.form["email"]
            password = request.form["password"]
            session["email"] = email
            return render_template("index.html", error = email)

@app.route("/prueba")
def prueba():
    nombres = []
    nombres.append({"nombre": "ruben",
    "Semestre01": [{
        "matematicas": "10",
        "español": "10"
    }],
    "Semestre02":[{
        "matemáticas":"10",
        "español": "10"
    }]})

    nombres.append({"nombre": "Sergio"})

    return render_template("home.html", data = nombres)

@app.route("/logout")
def logout():
    if "email" in session:
        session.clear()
        return redirect(url_for("home"))
