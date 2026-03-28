#Created by Luca Cottone on 3/28/26
'''Web app
Michigan residents can get legal help
    Renter's rights/property owners
    Small businesses
    Small Claims
    Injury
Made with Flask
Has chatbot interface as well
Attempting to win:
    best beginner
    best UI/UX
    Best use of Gemini API
'''
from flask import Flask, redirect, url_for, render_template, request, session # type: ignore
from datetime import timedelta
app = Flask(__name__)

@app.route("/") #root page
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)

@app.route("/Renters_Rights")
def renters_rights():
    return render_template("renters_rights.html")

@app.route("/Small_Businesses")
def small_businesses():
    return render_template("small_businesses.html")

@app.route("/Personal_Injury")
def personal_injury():
    return render_template("p_injury.html")

@app.route("/Small_Claims")
def small_claims():
    return render_template("s_claims.html")