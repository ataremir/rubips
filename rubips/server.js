const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');
const app = express();

app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Railway'den gelen kabloyu (URL) kontrol et
const connectionString = process.env.MYSQL_URL;

// Eğer kablo takılı değilse ekrana hata yazdır ama sistemi durdurma
if (!connectionString) {
    console.error("DİKKAT: MYSQL_URL bulunamadı! Lütfen Railway Variables kısmına ekle.");
}

// Veritabanı bağlantı havuzu (Pool) - En sağlam yöntem budur
const db = mysql.createPool(connectionString || "");

// MASA LİSTESİ ÇEKME
app.get('/api/masalar', (req, res) => {
    if (!connectionString) {
        return res.status(500).json({hata: "Veritabanı bağlantı kablosu (URL) eksik!"});
    }
    db.query('SELECT * FROM masalar ORDER BY id ASC', (err, results) => {
        if (err) return res.status(500).json(err);
        res.json(results);
    });
});

// YENİ MASA EKLEME
app.post('/api/masa-ekle', (req, res) => {
    const { id } = req.body; 
    db.query('INSERT INTO masalar (id, durum) VALUES (?, "bos")', [id], (err, result) => {
        if (err) return res.json({ hata: "Bu masa zaten var veya bir hata oluştu!" });
        res.json({ mesaj: "Masa başarıyla eklendi!" });
    });
});

// MASA SİLME
app.delete('/api/masa-sil/:id', (req, res) => {
    const id = req.params.id;
    db.query('DELETE FROM masalar WHERE id = ?', [id], (err, result) => {
        if (err) return res.json(err);
        res.json({ mesaj: "Masa dükkandan kaldırıldı!" });
    });
});

// SİSTEMİ BAŞLAT
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`🚀 Rubi PS Sistemi ${PORT} portunda başarıyla başlatıldı!`);
});
