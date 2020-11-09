from flask import Flask, Response, jsonify, request
from db import DB

app = Flask(__name__)

db = DB("submission_id", "listings")

@app.route('/')
def list():
    return jsonify(db.fetchall())

@app.route('/<item_id>')
def get(item_id):
    return jsonify(db.fetch(item_id))

@app.route('/', methods=['POST'])
def add():
    db.add(request.json)
    return Response(status=201)

@app.route('/<item_id>', methods=['DELETE'])
def delete(item_id):
    db.delete(item_id)
    return Response(status=204)

