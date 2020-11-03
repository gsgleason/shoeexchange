from flask import Flask, render_template
from db import Session
from models import Listing

app = Flask(__name__)

@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()

@app.route('/')
def index():
	listings = Session.query(Listing).all()
	return render_template('index.html', listings=listings)

