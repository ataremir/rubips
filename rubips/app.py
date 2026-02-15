@app.route('/api/personel-guncelle', methods=['POST'])
def update_staff():
    data = request.json
    user_id = data.get('userId')
    new_name = data.get('newName')
    new_pass = data.get('newPass')
    
    # Burada MySQL sorgusu ile kullanıcının ismi ve şifresi güncellenir
    # Örn: UPDATE users SET name=%s, pass=%s WHERE id=%s
    
    print(f"Sistem: Kullanıcı {user_id} güncellendi. Yeni Ad: {new_name}")
    return jsonify({"status": "success"})
