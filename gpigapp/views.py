from gpigapp import app
from flask import render_template, send_from_directory

@app.route('/')
def index():
    return render_template("index.html")




@app.route('/css/<path:path>')
def css(path):
    return send_from_directory('static/css', path)

@app.route('/img/<path:path>')
def img(path):
    return send_from_directory('static/img', path)
    
@app.route('/js/<path:path>')
def js(path):
    return send_from_directory('static/js', path)