from flask import Flask, request, redirect, url_for
from config import *

app = Flask(__name__)

@app.route('/')
def root ():
    return redirect(url_for('index'))

@app.route('/index')
def index ():
    return 'Hello World!'
