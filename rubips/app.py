import os
import json
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
DB_FILE = 'database.json'

# Varsayılan Veriler (İlk Kurulum)
default_data = {
    "settings": {"ps_rate": 150},
    "tables": [
        # Örnek: İlk 5 masa PS, sonraki 5 masa Nargile olsun
        {"id": 1, "name": "Masa 1", "type": "ps", "status": "bos", "orders": [], "start_time": None},
        {"id": 2, "name": "Masa 2", "type": "ps", "status": "bos", "orders": [], "start_time": None},
        {"id": 3, "name": "Masa 3", "type": "ps", "status": "bos", "orders": [], "start_time": None},
        {"id": 10, "name": "Loca 1", "type": "kafe", "status": "bos", "orders": [], "start_time": None},
        {"id": 11, "name": "Bahçe 1", "type": "kafe", "status": "bos", "orders": [], "start_time": None}
    ],
    "staff": []
}

def load_db():
    if not os.path.exists(DB_FILE):
        save_db(default_data)
        return default_data
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/get-data')
def get_data():
    return jsonify(load_db())

@app.route('/api/update-table', methods=['POST'])
def update_table():
    db = load_db()
    data = request.json
    for t in db['tables']:
        if t['id'] == data['id']:
            t.update(data)
            break
    save_db(db)
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
