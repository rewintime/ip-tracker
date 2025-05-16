from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

def get_db():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_ip', methods=['POST'])
def check_ip():
    ip = request.json.get('ip')
    conn = get_db()
    cur = conn.execute("SELECT * FROM ip_usage WHERE ip = ? ORDER BY datum DESC", (ip,))
    data = cur.fetchall()
    return jsonify([dict(row) for row in data])

@app.route('/save_ip', methods=['POST'])
def save_ip():
    ip = request.json.get('ip')
    anbieter = request.json.get('anbieter')
    datum = datetime.now().strftime('%d.%m.%Y')
    conn = get_db()
    for name in anbieter:
        conn.execute("INSERT INTO ip_usage (ip, anbieter, datum) VALUES (?, ?, ?)", (ip, name, datum))
    conn.commit()
    return jsonify({'success': True})
