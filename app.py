
from flask import Flask, render_template, request, session, redirect, url_for

import datetime 

import pymongo


# FlASK
#############################################################
app = Flask(__name__)

#Generar sesión de un año
app.permanent_session_lifetime = datetime.timedelta(days=365)
app.secret_key = "super secret key"

#############################################################


# Mongo DB
#############################################################
mongodb_key = "mongodb+srv://desarrollowebuser:desarrollowebpassword@cluster0.dfh7g.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(
    mongodb_key, tls=True, tlsAllowInvalidCertificates = True)
db = client.Escuela
cuentas = db.alumno
#############################################################






@app.route('/')
def home():

    if "email" in session:
        email = session["email"]
        return render_template('index.html', error = email)
    else:
        return render_template('login.html')


@app.route('/login', methods = ["GET", "POST"])
def login():
    if "email" in session:
        return render_template("index.html", error = session["email"])
    else:

        if(request.method == "GET"):
            return render_template("login.html")
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


@app.route("/usuarios")
def usuarios():
    cursor = cuentas.find({})
    users = []
    for doc in cursor:
        users.append(doc)
        return render_template("/usuarios.html", data = users)