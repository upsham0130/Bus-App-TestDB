from flask import Flask, url_for, render_template, request, jsonify, redirect
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
    students = NumberTable.query.all()
    return render_template("index.html", students=students)

@app.route('/addStudent', methods = ['POST'])
def addStudent():
    sName = request.form['sName']
    sID = request.form['sID']
    student = NumberTable(studentID = sID, studentName = sName)
    db.session.add(student)
    db.session.commit()

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)