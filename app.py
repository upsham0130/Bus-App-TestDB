from flask import Flask, url_for, render_template, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/addStudent', methods = ['POST'])
def addStudent():
    sName = request.form['sName']
    sID = request.form['sID']

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True) 