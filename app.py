from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret123"  # for sessions

# ---------------- DATABASE SETUP ---------------- #

def get_db():
    return sqlite3.connect('school.db')


def init_db():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            date TEXT
        )
    ''')

    conn.commit()
    conn.close()


# ---------------- AUTH ---------------- #

@app.route('/register', methods=['GET', 'POST'])
def register():
    error=None

    if request.method == 'POST':
        username = request.form['username']
        raw_password = request.form['password']

        if not username or not raw_password:
            error = "All fields are required"
        elif len(raw_password) < 4:
            error = "Password must be at least 4 characters"
        else:
            conn = get_db()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                error = "Username already exists"
            else:
                hashed_password = generate_password_hash(raw_password)
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
                conn.commit()
                conn.close()
                return redirect('/login')
        
        conn.close()

    return render_template('register.html',error=error)

# ---------------- LOGIN ---------------- #

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    user = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            error = "All fields are required"

        else:
            conn = get_db()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            user = cursor.fetchone()

            conn.close()

        if user and check_password_hash(user[2], password):
            session['user'] = username
            return redirect('/')
        elif request.method == 'POST':
            error = "Invalid username or password"

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')


# ---------------- HOME ---------------- #
@app.route('/')
def home():
    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, date FROM events ORDER BY date")
    events = cursor.fetchall()

    conn.close()

    return render_template('index.html', events=events, user=session['user'])

# ---------------- CGPA ---------------- #

@app.route('/cgpa', methods=['POST'])
def cgpa():
    courses = int(request.form['courses'])
    return render_template('cgpa.html', courses=courses)


@app.route('/calculate', methods=['POST'])
def calculate():
    courses = int(request.form['courses'])

    grade_dict = {'A':5, 'B':4, 'C':3, 'D':2, 'F':0}

    total_points = 0
    total_units = 0

    for i in range(courses):
        unit = int(request.form[f'unit{i}'])
        grade = request.form[f'grade{i}']

        total_points += grade_dict[grade] * unit
        total_units += unit

    cgpa = round(total_points / total_units, 2)

    return render_template('result.html', cgpa=cgpa)

# ---------------- EVENTS ---------------- #

@app.route('/add_event', methods=['POST'])
def add_event():
    title = request.form['title']
    date = request.form['date']

    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO events (title, date) VALUES (?, ?)", (title, date))

    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/delete/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events WHERE id=?", (event_id,))
    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/edit/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']

        cursor.execute("UPDATE events SET title=?, date=? WHERE id=?", (title, date, event_id))
        conn.commit()
        conn.close()

        return redirect('/')

    cursor.execute("SELECT title, date FROM events WHERE id=?", (event_id,))
    event = cursor.fetchone()
    conn.close()

    return render_template('edit.html', event=event, id=event_id)



# ---------------- RUN APP ---------------- #

if __name__ == '__main__':
    init_db()
    app.run(debug=True)



     
