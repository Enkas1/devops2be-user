from flask import Flask, request, render_template, url_for, session, redirect, jsonify
import os
import re
import psycopg2
from functions import *

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/", methods=["GET", "POST"])
def render_index():
    return render_template("index.html")

@app.route("/adminpage.html", methods=["POST", "GET", "PUT"])
def render_adminpage():
    activity = request.form.get("activity")
    price = request.form.get("price")
    
    
    if 'Lägg till en aktivitet' in request.form.values():
        if admin_add_activity(activity, price):
            return render_template("adminpage.html", message="Aktivitet tillagd")
        else:
            return render_template("adminpage.html", message="Något gick fel med att lägga till aktivitet")
              
    elif 'Ta bort aktivitet' in request.form.values():
        if admin_delete_activity(activity):
            return render_template("adminpage.html", message="Aktivitet raderad")
        else:
            return render_template("adminpage.html", message="Något gick fel med att radera aktiviteten")
    elif 'Nytt pris' in request.form.values():
        if admin_change_price(activity, price):
            return render_template("adminpage.html", message="Priset uppdaterat")
        else:
            return render_template("adminpage.html", message="Något gick fel med att uppdatera priset")

    return render_template("adminpage.html", message="Välkommen Admin")

@app.route("/inloggning.html", methods=["POST"])
def render_inloggning():
    return render_template("inloggning.html")

@app.route("/inloggad.html", methods=["POST", "GET"])
def render_inloggad():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        session["email"] = email

        if email and password: 
            if login_credentials_check(email, password):
                admin_status = admin_or_not(email)
                if admin_status:
                    return redirect(url_for('render_adminpage'))
                else:
                    return render_template("inloggad.html", message="Välkommen", email=email)
            else:
                return render_template("inloggning.html", message="Felaktiga inloggningsuppgifter. Var god försök igen eller skapa ett nytt konto")
        else:
            return render_template("inloggning.html")
    else:
        # Om det inte är en POST-förfrågan, returnera bara inloggningssidan
        return render_template("inloggning.html")
    
@app.route("/registration.html", methods=["POST", "GET"])
def render_registration():
    return render_template("registration.html") 

@app.route("/loginindex.html", methods=["GET"])
def render_loginindex():
    return render_template("loginindex.html")

@app.route("/registrationstatus.html", methods=["GET", "POST"])
def register_user_status():
    email = request.form.get("email")
    password = request.form.get("password")
    phone = request.form.get("phone")
    input_data = (email, password, phone)

    # Regex-mönster för att validera e-postadress
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    # Regex-mönster för att validera password (minst 5 tecken)
    password_pattern = r"^(?=\s*\S)(.{5,}(?:\s+\S+){0,30}\s*)$"
    # Regex-mönster för att validera telefonnummer (exakt 10 siffror)
    phone_pattern = r"^\d{10}$"
    

    # Validera e-postadress
    if not re.match(email_pattern, request.form["email"]):
        return render_template("/registration.html", message="<span style='color: white;'>Felaktig e-postadress!</span>")

    # Validera telefonnummer
    if not re.match(phone_pattern, request.form["phone"]):
        return render_template("/registration.html", message="<span style='color: white;'>Felaktigt telefonnummer, fyll i 10 siffror!</span>")

    # Validera meddelandet
    if not re.match(password_pattern, request.form["password"]):
        return render_template("/registration.html", message="<span style='color: white;'>Lösenordet behöver vara minst 5 tecken långt!</span>")

    if input_data:
        try:
            conn = psycopg2.connect(**conn_details)
            cur = conn.cursor()
            cur.execute("INSERT INTO inloggningsuppgifter (email, password, phone) VALUES (%s, %s, %s)",
                        (email, password, phone))
            conn.commit()
            cur.close()
            conn.close()
            return render_template("registrationstatus.html", message="Konto skapat, var god logga in")
        except psycopg2.Error as e:
            print("Error inserting user information:", e)
            return render_template("registrationstatus.html", message="Ett fel uppstod vid registreringen. Vänligen försök igen senare.")
    else:
        return render_template("registrationstatus.html", message="Nödvändiga uppgifter saknas")

 



if __name__ == "__main__":
    app.run(debug=True) 