# from extra import a

import os
import json
from flask import request

from flask import Flask, render_template, session, redirect
from functools import wraps
import pymongo

app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'

# Database
# client = pymongo.MongoClient('localhost', 27017)

# usr = os.environ['voyager']
# pwd = os.environ['hubbble']

client = pymongo.MongoClient("mongodb+srv://voyager:hubble@cluster0.fjqikim.mongodb.net/?retryWrites=true&w=majority")
db = client.user_login_system

# Decorators
def login_required(f):
  print(f)
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')
  
  return wrap

# Routes
from user import routes

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/dashboard/')
@login_required
def dashboard():
  return render_template('new.html')


# @app.route('/upload/')
# @login_required
# def upload():
#   return render_template('upload.html')


app.config["UPLOAD_DIR"] = "uploads"
@app.route("/upload/", methods = ["GET", "POST"])
@login_required
def upload():
  print(request.method)
  if request.method == 'POST':
      file = request.files['file']
      file.save(os.path.join(app.config['UPLOAD_DIR'], file.filename))
      return render_template("upload.html", msg = "File uplaoded successfully.")
  return render_template("upload.html", msg = "")
    

# @app.route('/verification/')
# @login_required
# def verification():
#   return render_template('verification.html')


app.config["UPLOAD_DIR"] = "uploads_doc"
@app.route("/verification/", methods = ["GET", "POST"])
@login_required
def verification():
  print(request.method)
  if request.method == 'POST':
      file = request.files['file']
      file.save(os.path.join(app.config['UPLOAD_DIR'], file.filename))
      return render_template("verification.html", msg = "File uplaoded successfully.")
  return render_template("verification.html", msg = "")


@app.route('/profile/')
@login_required
def profile():
  return render_template('profile.html')

@app.route('/contact/')
@login_required
def contact():
  return render_template('contact.html')


  if __name__ == "__main__":
    app.run(debug=True)