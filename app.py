from flask import Flask, render_template
from db import DB
from datetime import datetime

app = Flask(__name__)

db = DB("submission_id", "listings")

@app.route('/')
def index():
    listings = db.fetchall()
    print(listings[0])
    return render_template('index.html', listings=listings, datetime=datetime, int=int)

