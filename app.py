
from flask import Flask, render_template, request, session, redirect, url_for

import datetime 

import pymongo

from twilio.rest import Client



# FlASK
#############################################################
app = Flask(__name__)

#Generar sesión de un año
app.permanent_session_lifetime = datetime.timedelta(days=365)
app.secret_key = "super secret key"

#############################################################


# Mongo DB
#############################################################
mongodb_key = "mongodb+srv://testUser123:123Pass@cluster0.fyhsi.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(
    mongodb_key, tls=True, tlsAllowInvalidCertificates = True)
db = client.Escuela
cuentas = db.alumno
#############################################################


# Twilio
#############################################################
#account_sid = ""
#auth_token = ""
#TwilioClient = Client(account_sid, auth_token)
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
            #registrationNo = request.form["matricula"]
            password = request.form["password"]
            userSearch = cuentas.find_one({"correo": (email), "contrasena": (password)}) #Check database for finding email and password that matches
            if userSearch != None:
                  session["email"] = email
                  return render_template("index.html", error = email)
                  
            else:
                 return render_template('login.html', data = None)
              

            

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

@app.route("/insert", methods = ["POST"])
def insertUsers():

    user = {
        "matricula": request.form["matricula"],
        "nombre":request.form['nombre'],
        "correo":request.form['correo'],
        "contrasena": request.form['contrasena'],
    }

    try:
        cuentas.insert_one(user)
        
        """comogusten = TwilioClient.messages.create(
            from_="whatsapp:+14155238886",
            body="El usuario %s se agregó a tu pagina web" % (
                request.form["nombre"]),
            to="whatsapp:+5215514200581"
        )
        print(comogusten.sid)"""

        return redirect(url_for("usuarios"))

    except Exception as e:
        return "<p>El servicio no está disponible =>: %s %s" % type(e), e


@app.route("/find_one/<matricula>")
def find_one(matricula):
    try:
        user = cuentas.find_one({"matricula": (matricula)})
        if user == None:
            return "<p>La matricula %s no existe</p>" % (matricula)
        else:
            return "<p>Encontramos: %s </p>" % (user)
    except Exception as e:
        return "%s" % e

@app.route("/delete/<matricula>")
def delete_one(matricula):
    try:
        user = cuentas.delete_one({"matricula": (matricula)})
        if user.deleted_count == None:
            return "<p>La matricula %s no existe</p>" % (matricula)
        else:
            #return "<p>Eliminamos %d matricula: %s </p>" % (user.deleted_count, matricula)
            return redirect(url_for("usuarios"))
    except Exception as e:
        return "%s" % e

@app.route("/update", methods = ["POST"])


def update():
    try:
        filter = {"matricula": request.form["matricula"]} #Create a search object
        user = {"$set": {
            "nombre": request.form["matricula"], #only update field matricula
            "contrasena": request.form["contrasena"]
        }}
        cuentas.update_one(filter, user)
        return redirect(url_for("usuarios"))

    except Exception as e:
        return "%s" % e

@app.route('/create')
def create():
    return render_template('Create.html')