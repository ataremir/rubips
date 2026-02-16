import os
import json
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# VERİTABANI DOSYASI
DB_FILE = 'data.json'

# Varsayılan Veriler (İlk açılışta oluşturulur)
default_data = {
    "settings": {"ps_rate": 120},
    "tables": [],
    "staff": [
        {"id": 1, "name": "Admin", "role": "admin", "pass": "1907", "sales": 0},
        {"id": 2, "name": "Garson", "role": "garson", "pass": "1234", "sales": 0}
    ]
}

def load_db():
    if not os.path.exists(DB_FILE):
        save_db(default_data)
        return default_data
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

@app.route('/')
def index():
    return render_template('index.html')

# --- API: GİRİŞ ---
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    db = load_db()
    user = next((u for u in db['staff'] if u['name'] == data['name'] and u['pass'] == data['pass']), None)
    if user:
        return jsonify({"status": "success", "user": user})
    return jsonify({"status": "fail"}), 401

# --- API: PERSONEL İŞLEMLERİ ---
@app.route('/api/staff', methods=['GET', 'POST'])
def staff_ops():
    db = load_db()
    if request.method == 'GET':
        return jsonify(db['staff'])
    
    if request.method == 'POST': # Yeni Personel Ekle
        new_staff = request.json
        new_staff['id'] = len(db['staff']) + 1
        new_staff['sales'] = 0
        db['staff'].append(new_staff)
        save_db(db)
        return jsonify({"status": "success"})

@app.route('/api/staff/update', methods=['POST'])
def staff_update():
    data = request.json
    db = load_db()
    for s in db['staff']:
        if s['id'] == data['id']:
            s['name'] = data.get('name', s['name'])
            s['pass'] = data.get('pass', s['pass'])
            s['role'] = data.get('role', s['role'])
    save_db(db)
    return jsonify({"status": "success"})

# --- API: SATIŞ YAP (CİRO EKLE) ---
@app.route('/api/sale', methods=['POST'])
def add_sale():
    data = request.json
    db = load_db()
    # Personel cirosunu artır
    for s in db['staff']:
        if s['id'] == data['staff_id']:
            s['sales'] += float(data['amount'])
    save_db(db)
    return jsonify({"status": "success"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
