from myportfolio import app
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def bio():
    return render_template('bio.html')

@app.route('/timeline')
def timeline():
    return render_template('timeline.html')