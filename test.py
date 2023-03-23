import mysql.connector
db=mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="1234",
    auth_plugin='mysql_native_password',
    database="testdatabase"

)

mycursor=db.cursor()
# mycursor.execute("CREATE DATABASE testdatabase")

# mycursor.execute('''Create table dept(
#     dept_id integer,
#     dept_name varchar(20),
#     faculty varchar(30),
#     no_of_student integer,
#     primary key(dept_id)
#     );''')

# mycursor.execute('describe dept')
# for x in mycursor:
#     print(x)
# mycursor.execute("INSERT INTO dept (dept_id,dept_name,faculty,no_of_student) VALUES (3,'EEE','EE',120)")
# val = (3,'EEE','EE',120)
# mycursor.execute(sql)
# db.commit()
# mycursor.execute('show tables')
mycursor.execute('select * from dept')
for x in mycursor:
    print(x)