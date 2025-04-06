
from flask import Flask, render_template, request, redirect, jsonify

from utils.db import db

from models.student import *


app =  Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Student.db'

@app.route('/')
def index():
    student = Student.query.all()
    return render_template('index.html',  content=student)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    students = Student.query.all()  # ORM query to fetch student data
    students_data = [{
        'id': student.id,
        'name': student.name,
        'maths': student.maths,
        'biology': student.biology,
        'social': student.social,
        'percentage': student.percentage
    } for student in students]
    return render_template('dashboard.html', content=students_data)


@app.route('/add_student')
def add_student():
    return render_template('add_student.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/submit', methods=['POST'])
def submit():
    form_data = request.form.to_dict()
    print(f"form_data: {form_data}")

    id = form_data.get('id')
    name = form_data.get('name')
    maths = float(form_data.get('maths'))
    biology = float(form_data.get('biology'))
    social = float(form_data.get('social'))

    # Calculate the percentage
    total_marks = maths + biology + social
    total_possible_marks = 300  # Assuming each subject is out of 100
    percentage = (total_marks / total_possible_marks) * 100

    # Insert data into the database
    student = Student.query.filter_by(id=id).first()
    if not student:
        student = Student(id=id, name=name, maths=maths, biology=biology, social=social,
                          percentage=round(percentage, 2))
        db.session.add(student)
        db.session.commit()
    print("Submitted successfully")
    return redirect('/')


@app.route('/delete/<int:id>', methods=['GET', 'DELETE'])
def delete(id):
    student = Student.query.get(id)
    print("task: {}".format(student))

    if not student:
        return jsonify({'message': 'student not found'}), 404
    try:
        db.session.delete(student)
        db.session.commit()
        return jsonify({'message': 'student deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while deleting the data {}'.format(e)}), 500


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    student = Student.query.get_or_404(id)
    print(student.id)
    if not student:
        return jsonify({'message': 'student not found'}), 404

    if request.method == 'POST':
        student.id = request.form['id']
        student.name = request.form['name']
        student.maths = request.form['maths']
        student.biology = request.form['biology']
        student.social = request.form['social']
        student.percentage = request.form['percentage']

        try:
            db.session.commit()
            return redirect('/')

        except Exception as e:
            db.session.rollback()
            return "there is an issue while updating the record"
    return render_template('update.html', student=student)


if __name__ =='__main__':
    app.run(debug=True)
