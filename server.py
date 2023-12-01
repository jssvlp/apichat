import os
from flask import Flask, send_from_directory, render_template, redirect, send_file
import chats
import utils


app = Flask(__name__)

port = int(os.environ.get("PORT", 5000))



@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/chats')
def chat():
    chat = chats.parseFlatFile()

    data = { 
            "success" : True, 
            "data" : chat, 
    } 

    return data

@app.route('/file/<path:path>')  
def file(path):
    full_path = "static/media/" + path

    mimetype = utils.get_mimetype(path)

    return send_file(full_path, mimetype=mimetype)

@app.route('/<path:path>')
def all_routes(path):
    return redirect('/')

if __name__ == "__main__":
    app.run(port=port)