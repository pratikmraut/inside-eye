# from extra import a

import os
import json
from flask import request
import glob
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import pandas as pd
import pathlib
from flask import Flask, render_template, session, redirect
from functools import wraps
import pymongo


import tika
tika.initVM()
from tika import parser

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

@app.route('/home1')
def signUp():
  return render_template('home1.html')

# @app.route('/home1/')
# def home1():
#   return render_template('home1.html')

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


app.config["UPLOAD_DIR"] = "uploads"
@app.route("/verification/", methods = ["GET", "POST"])
@login_required
def verification():
  
  print(request.method)

  def read_qr_code(filename):
    image = cv2.imread(os.path.join(app.config['UPLOAD_DIR'], filename))

    decodedObjects = pyzbar.decode(image)
    for obj in decodedObjects:
        # print("Type: QRCODE")
        # print("Data:  b'www.copyassignment.com'")
        print("Type:", obj.type)
        print("Data: ", obj.data, "\n")
  def resume(filename):
    file_data = parser.from_file(os.path.join(app.config['UPLOAD_DIR'], filename))
    text = file_data['content']
    print(text)

  if request.method == 'POST':
      file = request.files['file']
      file.save(os.path.join(app.config['UPLOAD_DIR'], file.filename))
      # print(read_qr_code(file.filename))
      resume(file.filename)

      return render_template("verification.html", msg = "File uplaoded successfully.")
  return render_template("verification.html", msg = "")


@app.route('/profile/' , methods = ["GET", "POST"])
@login_required
def profile():
  return render_template('profile.html')

@app.route('/contact/')
@login_required
def contact():
  return render_template('contact.html')



if __name__ == "__main__":
  app.run(debug=True)