from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# DB Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Mydata@123'
app.config['MYSQL_DB'] = 'studentdb'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template("form.html")


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    courses = request.form.getlist('course')
    courses = ", ".join(courses)
    education = request.form['education']

    conn = mysql.connection
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO students(name, phone, email, course, education) VALUES(%s, %s, %s, %s, %s)",
        (name, phone, email, courses, education)
    )

    conn.commit()
    cursor.close()

    return "✔ Record Added Successfully!"


@app.route('/view')
def view():
    return render_template("view.html")


@app.route('/getdetails', methods=['POST'])
def getdetails():
    phone = request.form['phone']

    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE phone=%s", (phone,))
    data = cursor.fetchone()
    cursor.close()

    return render_template("view.html", data=data)


@app.route('/list')
def list_all():
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    cursor.close()

    return render_template("list.html", data=data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
