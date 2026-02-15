from flask import Flask, render_template, jsonify, request
import os

app = Flask(__name__)

# Personel Veritabanı (Şimdilik RAM'de duruyor, restart atınca sıfırlanır)
# MySQL'e geçtiğimizde burası veritabanından okunacak.
personeller = [
    {"id": 1, "isim": "Garson Ali", "rol": "garson", "sifre": "1234", "satis": 1450},
    {"id": 2, "isim": "Nargileci Memo", "rol": "garson", "sifre": "1234", "satis": 850},
    {"id": 3, "isim": "Admin", "rol": "admin", "sifre": "1907", "satis": 0}
]

@app.route('/')
def index():
    return render_template('index.html')

# 1. PERSONEL LİSTESİNİ GÖNDER
@app.route('/api/personel-listesi', methods=['GET'])
def get_staff():
    return jsonify(personeller)

# 2. YENİ PERSONEL EKLE (Bunu Ekledik)
@app.route('/api/personel-ekle', methods=['POST'])
def add_staff():
    data = request.json
    yeni_id = len(personeller) + 1
    yeni_kullanici = {
        "id": yeni_id,
        "isim": data.get('isim'),
        "rol": data.get('rol'),
        "sifre": data.get('sifre'),
        "satis": 0
    }
    personeller.append(yeni_kullanici)
    return jsonify({"status": "success", "message": "Personel eklendi", "user": yeni_kullanici})

# 3. PERSONEL BİLGİSİ GÜNCELLE (Bunu Ekledik)
@app.route('/api/personel-guncelle', methods=['POST'])
def update_staff():
    data = request.json
    hedef_id = int(data.get('id'))
    
    for p in personeller:
        if p['id'] == hedef_id:
            p['isim'] = data.get('isim')
            p['sifre'] = data.get('sifre')
            p['rol'] = data.get('rol')
            return jsonify({"status": "success", "message": "Güncellendi"})
            
    return jsonify({"status": "error", "message": "Kullanıcı bulunamadı"}), 404

# 4. SATIŞ EKLE
@app.route('/api/satis-ekle', methods=['POST'])
def add_sale():
    data = request.json
    # İleride buraya MySQL UPDATE komutu gelecek
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
