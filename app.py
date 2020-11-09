from flask import Flask, render_template, request, jsonify
from db import DB

app = Flask(__name__)

db = DB("submission_id", "listings")

@app.route('/')
def index():
    listings = db.fetchall()
    if "application/json" in request.headers['accept'].split(","):
        return jsonify(listings)
    return render_template('index.html', listings=listings)

