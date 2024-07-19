from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
import csv

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS admissions (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            course TEXT,
                            session TEXT,
                            ining TEXT,
                            from_date TEXT,
                            to_date TEXT,
                            student_name TEXT,
                            father_name TEXT,
                            mother_name TEXT,
                            dob TEXT,
                            gender TEXT,
                            contact_no TEXT,
                            email TEXT,
                            permanent_address TEXT,
                            correspondence_address TEXT,
                            education TEXT)''')
        conn.commit()

init_db()

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        data = (request.form['course'], request.form['session'], request.form['ining'], 
                request.form['from_date'], request.form['to_date'], request.form['student_name'],
                request.form['father_name'], request.form['mother_name'], request.form['dob'],
                request.form['gender'], request.form['contact_no'], request.form['email'],
                request.form['permanent_address'], request.form['correspondence_address'],
                request.form['education'])
        
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO admissions (course, session, ining, from_date, to_date, student_name, 
                                                     father_name, mother_name, dob, gender, contact_no, email, 
                                                     permanent_address, correspondence_address, education)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)
            conn.commit()
        
        return redirect(url_for('index'))

@app.route('/view_records')
def view_records():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admissions")
        records = cursor.fetchall()
    return render_template('view_records.html', records=records)

@app.route('/edit_record/<int:record_id>', methods=['GET', 'POST'])
def edit_record(record_id):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        if request.method == 'POST':
            data = (request.form['course'], request.form['session'], request.form['ining'], 
                    request.form['from_date'], request.form['to_date'], request.form['student_name'],
                    request.form['father_name'], request.form['mother_name'], request.form['dob'],
                    request.form['gender'], request.form['contact_no'], request.form['email'],
                    request.form['permanent_address'], request.form['correspondence_address'],
                    request.form['education'], record_id)
            
            cursor.execute('''UPDATE admissions
                              SET course = ?, session = ?, ining = ?, from_date = ?, to_date = ?, student_name = ?, 
                                  father_name = ?, mother_name = ?, dob = ?, gender = ?, contact_no = ?, email = ?, 
                                  permanent_address = ?, correspondence_address = ?, education = ?
                              WHERE id = ?''', data)
            conn.commit()
            return redirect(url_for('view_records'))
        else:
            cursor.execute("SELECT * FROM admissions WHERE id = ?", (record_id,))
            record = cursor.fetchone()
            return render_template('edit_record.html', record=record)

@app.route('/export_records')
def export_records():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admissions")
        records = cursor.fetchall()
    
    with open('records.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['ID', 'Course', 'Session', 'Ining', 'From Date', 'To Date', 'Student Name', 'Father Name',
                            'Mother Name', 'DOB', 'Gender', 'Contact No', 'Email', 'Permanent Address', 
                            'Correspondence Address', 'Education'])
        csvwriter.writerows(records)
    
    return send_file('records.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
