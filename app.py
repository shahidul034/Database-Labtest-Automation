from flask import Flask, render_template,request,flash,redirect,url_for
import mysql.connector
import requests
app = Flask(__name__)
app.secret_key = "my_secret_key"
@app.route('/')
def dept_input():
    return render_template('index.html')

def sql_con():
    import cx_Oracle
    con = cx_Oracle.connect('ss15/p1234@localhost')
    cursor = con.cursor()
    return con,cursor
def table_creation(mycursor):
    
    # Check if dept table exists
    mycursor.execute("SELECT COUNT(*) FROM user_tables WHERE table_name = 'DEPT'")
    dept_table_exists = mycursor.fetchone()[0]
    print(dept_table_exists)
    if not dept_table_exists:
        mycursor.execute('''
            CREATE TABLE dept (
                dept_id INT,
                dept_name VARCHAR(20),
                faculty VARCHAR(30),
                no_of_student INT,
                PRIMARY KEY(dept_id)
            )
        ''')

    # Check if course table exists
    mycursor.execute("SELECT COUNT(*) FROM user_tables WHERE table_name = 'COURSE'")
    course_table_exists = mycursor.fetchone()[0]

    if not course_table_exists:
        mycursor.execute('''
            CREATE TABLE course (
                course_no VARCHAR(20),
                course_name VARCHAR(50),
                year_semester INT,
                credit DECIMAL(20,4),
                dept_id INT,
                PRIMARY KEY(course_no),
                FOREIGN KEY(dept_id) REFERENCES dept(dept_id)
            )
        ''')

    # Check if book table exists
    mycursor.execute("SELECT COUNT(*) FROM user_tables WHERE table_name = 'BOOK'")
    book_table_exists = mycursor.fetchone()[0]

    if not book_table_exists:
        mycursor.execute('''
            CREATE TABLE book (
                book_no INT,
                book_name VARCHAR(50),
                author VARCHAR(50),
                book_edition INT,
                course_offering INT,
                PRIMARY KEY(book_no)
            )
        ''')

    # Check if relation table exists
    mycursor.execute("SELECT COUNT(*) FROM user_tables WHERE table_name = 'RELATION'")
    relation_table_exists = mycursor.fetchone()[0]

    if not relation_table_exists:
        mycursor.execute('''
            CREATE TABLE relation (
                book_no INT,
                course_no VARCHAR(20),
                PRIMARY KEY(book_no, course_no),
                FOREIGN KEY(book_no) REFERENCES book(book_no),
                FOREIGN KEY(course_no) REFERENCES course(course_no)
            )
        ''')
@app.route('/create-table', methods=['GET','POST'])
def table_create():
    con,mycursor=sql_con()
    table_creation(mycursor)
    flash("sucessfully created table!!!")
    print("sucessfully created table!!!")
    return redirect(url_for('dept_input'))
    

@app.route('/dept-submit', methods=['GET','POST'])
def dept_submit():
    dept_id = request.form['dept_id']
    dept_name = request.form['dept_name']
    faculty = request.form['faculty']
    no_of_student = request.form['no_of_student']
    con,mycursor=sql_con()
    # table_creation(mycursor)
    data=f"INSERT INTO dept (dept_id, dept_name, faculty, no_of_student) VALUES ({dept_id}, '{dept_name}', '{faculty}', {no_of_student})"
    # print(data)
    try:
        mycursor.execute(data)
        mycursor.execute("select * from dept")
        for x in mycursor:
            print(x)
        con.commit()
        return "Data inserted successfully"
        
    except:
        print("Primary Key error!!!")
    
    


    
    

if __name__ == "__main__":
    app.run(debug=True)