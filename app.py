from flask import Flask, url_for, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)

class NumberTable(db.Model):
    index = db.Column(db.Integer, primary_key=True)
    studentID = db.Column(db.Integer)
    studentName = db.Column(db.String)

@app.route('/')
def index():
    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True)