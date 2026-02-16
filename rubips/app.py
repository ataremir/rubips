import os
import json
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# VERİTABANI DOSYASI
DB_FILE = 'database.json'

# Varsayılan Veriler (İlk açılışta)
default_data = {
    "settings": {"ps_rate": 120},
    "tables": [{"id": i, "name": f"Masa {i}", "type": "ps", "status": "bos", "orders": [], "start_time": None} for i in range(1, 9)],
    "staff": [
        {"id": 1, "name": "Admin", "role": "admin", "pass": "1907"},
        {"id": 2, "name": "Garson Ali", "role": "garson", "pass": "1234"}
    ],
    "products": [
        {"id": 1, "name": "Çay", "price": 20},
        {"id": 2, "name": "Kahve", "price": 40}
    ]
}

# Verileri Yükle
def load_db():
    if not os.path.exists(DB_FILE):
        save_db(default_data)
        return default_data
    with open(DB_FILE, 'r') as f:
        return json.load(f)

# Verileri Kaydet
def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

# --- API (Cihazların Konuştuğu Yer) ---

@app.route('/api/get-all')
def get_all():
    return jsonify(load_db())

@app.route('/api/update-table', methods=['POST'])
def update_table():
    db = load_db()
    data = request.json
    table_id = data.get('id')
    
    for t in db['tables']:
        if t['id'] == table_id:
            t.update(data) # Masayı güncelle
            break
            
    save_db(db)
    return jsonify({"status": "ok"})

@app.route('/api/update-settings', methods=['POST'])
def update_settings():
    db = load_db()
    new_rate = request.json.get('ps_rate')
    db['settings']['ps_rate'] = float(new_rate)
    save_db(db)
    return jsonify({"status": "ok"})

@app.route('/api/add-staff', methods=['POST'])
def add_staff():
    db = load_db()
    new_user = request.json
    new_user['id'] = len(db['staff']) + 1
    db['staff'].append(new_user)
    save_db(db)
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
