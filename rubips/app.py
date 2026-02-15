import os
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Buraya daha sonra Gider ve Porsiyon API'lerini ekleyeceğiz
@app.route('/api/status')
def status():
    return jsonify({"durum": "TCFH/SOFT Aktif", "versiyon": "5.0"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
