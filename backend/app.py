from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 🔑 MySQL Config (CHANGE PASSWORD)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Avni@4070'   # your password
app.config['MYSQL_DB'] = 'mannsetu'

mysql = MySQL(app)

# ================= USER REGISTER =================
@app.route('/register', methods=['POST'])
def register():
    data = request.json

    phone = data['phone']
    name = data['name']
    age = data['age']
    gender = data['gender']

    cur = mysql.connection.cursor()

    # 🔍 Check if phone already exists
    cur.execute("SELECT * FROM users WHERE phone=%s", (phone,))
    existing = cur.fetchone()

    if existing:
        return jsonify({"message": "Phone already exists ❌"})

    # ✅ Insert new user
    cur.execute(
        "INSERT INTO users (phone, name, age, gender) VALUES (%s, %s, %s, %s)",
        (phone, name, age, gender)
    )

    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "User Registered ✅"})

# ================= ADD TASK =================
@app.route('/task', methods=['POST'])
def add_task():
    data = request.json

    phone = data['phone']
    task = data['task']
    priority = data['priority']
    date = data['date']

    cur = mysql.connection.cursor()

    cur.execute(
        "INSERT INTO tasks (phone, task, priority, date) VALUES (%s, %s, %s, %s)",
        (phone, task, priority, date)
    )

    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Task Saved ✅"})

# ================= GET TASKS =================
@app.route('/tasks/<phone>', methods=['GET'])
def get_tasks(phone):
    cur = mysql.connection.cursor()

    cur.execute("SELECT task, priority, date FROM tasks WHERE phone=%s", (phone,))
    data = cur.fetchall()

    cur.close()

    return jsonify(data)

# ================= JOURNAL =================
@app.route('/journal', methods=['POST'])
def journal():
    data = request.json

    phone = data['phone']
    entry = data['entry']

    cur = mysql.connection.cursor()

    cur.execute(
        "INSERT INTO journal (phone, entry) VALUES (%s, %s)",
        (phone, entry)
    )

    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Journal Saved ✅"})

# ================= RUN =================
if __name__ == '__main__':
    app.run(debug=True)