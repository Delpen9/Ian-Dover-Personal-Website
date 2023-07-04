from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def bio():
    return render_template('bio.html')

@app.route('/timeline')
def timeline():
    return render_template('timeline.html')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug = True, host = '0.0.0.0', port = port)