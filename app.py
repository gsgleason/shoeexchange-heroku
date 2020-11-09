from flask import Flask, render_template
from db import DB
from datetime import datetime

app = Flask(__name__)

db = DB("submission_id", "listings")

@app.route('/')
def index():
    listings = db.fetchall()
    last_updated = datetime.fromtimestamp(listings[0]['updated_utc']).isoformat()
    return render_template('index.html', listings=listings, datetime=datetime)

