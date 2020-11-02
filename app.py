from flask import Flask, render_template
from db import Session
from models import Listing

app = Flask(__name__)

@app.teardown_appcontext
def cleanup(resp_or_exc):
    Session.remove()

@app.route('/')
def index():
	listings = Session.query(Listing).all()
	return render_template('index.html', listings=listings)

