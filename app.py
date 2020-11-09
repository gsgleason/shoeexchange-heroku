from flask import Flask, render_template
from db import DB

app = Flask(__name__)

db = DB("submission_id", "listings")

@app.route('/')
def index():
    listings = db.fetchall()
    return render_template('index.html', listings=listings)

