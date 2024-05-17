import os
from flask import Flask, send_from_directory, render_template, redirect, send_file, request, jsonify
import chats
import utils
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app)


cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})

port = int(os.environ.get("PORT", 5000))


@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/chats')
def chat():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=100, type=int)  # Number of items per page
    data = chats.get_paginated_data(page, per_page)
    return data
    

@app.route('/file/<path:path>')  
def file(path):
    full_path = "static/media/" + path

    mimetype = utils.get_mimetype(path)

    if( mimetype == 'audio/opus'):
        path = path.replace('.opus','.m4a')
        full_path = "static/media/voice/" + path
        mimetype = utils.get_mimetype(path)

    return send_file(full_path, mimetype=mimetype)

@app.route('/<path:path>')
def all_routes(path):
    return redirect('/')

if __name__ == "__main__":
    app.run(port=port)