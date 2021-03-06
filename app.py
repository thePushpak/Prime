import math
import time
import sqlite3 as sql
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Creating database named prime_num.db
# Using SQLITE3 internal database
# Creating table named PrimeGenerator to stored updated value
# Handling sql.OperationError to avoid creating database file again and again
conn = sql.connect('prime_num.db')
try:
    conn.execute("create table PrimeGenerator (id INTEGER PRIMARY KEY AUTOINCREMENT, lower INTEGER, upper INTEGER,"
                 "time_elapsed INTEGER, No_of_Primes INTEGER, Timestamp DATETIME)")
    conn.commit()
except sql.OperationalError:
     None


# Function for Prime number Generator One
# using time library to get execution time of Prime Generator 1 operation
def prime_gen_1(num1, num2):
    list_1, total = [], 0
    t0 = time.time()
    for num in range(num1, num2 + 1):
        # all prime numbers are greater than 1
        if num > 1:
            for i in range(2, num):
                if (num % i) == 0:
                    break
            else:
                list_1.append(str(num))
    t1 = time.time()
    execution = t1-t0
    total = len(list_1)
    # Printing Execution time of code and Total of Prime numbers
    print(f"Execution time: {execution} and Total num: {total}")
    with sql.connect("prime_num.db") as con:
        cur = con.cursor()
        cur.execute("INSERT into PrimeGenerator (time_elapsed, No_of_Primes, lower, upper, Timestamp) values (?,?,?,"
                    "?,?)", (execution, total, num1, num2, time.strftime('%Y-%m-%d - %H:%M')))
        con.commit()
    return ", ".join(list_1)


# Function for Prime number Generator Two
# using time library to get execution time of Prime Generator 2 operation
def prime_gen_2(num1, num2):
    list_2, total = [], 0
    t0 = time.time()
    for num in range(num1, num2):
        if all(num % i != 0 for i in range(2, int(math.sqrt(num)) + 1)):
            list_2.append(str(num))
    t1 = time.time()
    execution = t1 - t0
    total = len(list_2)
    # Printing Execution time of code and Total of Prime numbers
    print(f"Execution time: {execution} and Total num: {len(list_2)}")
    # storing values in database
    with sql.connect("prime_num.db") as con:
        cur = con.cursor()
        cur.execute("INSERT into PrimeGenerator (time_elapsed, No_of_Primes, lower, upper, Timestamp) values (?,?,?,"
                    "?,?)", (execution, total, num1, num2, time.strftime('%Y-%m-%d - %H:%M')))
        con.commit()
    return ", ".join(list_2)


# Index page route
@app.route("/")
def hello():
    # To choose between different generators html.html file created
    return render_template("html.html")


# Route of Prime number Generator One
# Both POST and GET method are used
@app.route("/gen_one/", methods=["GET", "POST"])
def gen_1():
    # Handling the POST request
    if request.method == 'POST':
        lower = request.form['no_1']
        upper = request.form['no_2']
        return redirect(url_for('detect_prime_1', num1=lower, num2=upper))

    # Handling the GET request
    return '''
                <form method="POST">
                    <div><label>Smaller number: <input type="number" name="no_1"></label></div><br>
                    <div><label>Larger number: <input type="text" name="no_2"></label></div><br>
                    <input type="submit" value="Submit">
                </form>'''


# Route of Prime number Generator Two
# Both POST and GET method are used
@app.route("/gen_two/", methods=["POST", "GET"])
def gen_2():
    # Handling the POST request
    if request.method == 'POST':
        lower = request.form['no_1']
        upper = request.form['no_2']
        return redirect(url_for('detect_prime_2', num1=lower, num2=upper))

    # Handling the GET request
    return '''
                <form method="POST">
                    <div><label>Smaller number: <input type="number" name="no_1"></label></div><br>
                    <div><label>Larger number: <input type="text" name="no_2"></label></div><br>
                    <input type="submit" value="Submit">
                </form>'''


# Printing Prime numbers using Prime Generator One
@app.route("/gen_one/<int:num1>/<int:num2>")
def detect_prime_1(num1, num2):
    # If number 1 is greater than number 2 in input Range then redirect to input page
    # If both numbers are same then redirect to input page
    if num1 >= num2:
        print('invalid entries')
        return redirect(url_for('gen_1'))
    else:
        return 'The Prime numbers between %d and %d are: %s' % (num1, num2, prime_gen_1(num1, num2))


# Printing Prime numbers using Prime Generator Two
@app.route("/gen_two/<int:num1>/<int:num2>")
def detect_prime_2(num1, num2):
    # If number 1 is greater than number 2 in input Range then redirect to input page
    # If both numbers are same then redirect to input page
    if num1 >= num2:
        print('invalid entries')
        return redirect(url_for('gen_2'))
    else:
        return 'The Prime numbers between %d and %d are: %s' % (num1, num2, prime_gen_2(num1, num2))


if __name__ == '__main__':
    # Run Flask server
    app.run(port=5000, debug=True, threaded=True)
