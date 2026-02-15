const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');
const app = express();

app.use(cors());
app.use(express.json());
app.use(express.static('public'));

const db = mysql.createPool(process.env.MYSQL_URL);

// MASALARI VE KALAN SÜRELERİ GETİR
app.get('/api/masalar', (req, res) => {
    const sql = `SELECT *, 
        CASE 
            WHEN durum = 'dolu' THEN ROUND(60 - (TIMESTAMPDIFF(SECOND, baslangic_zamani, NOW()) / 60))
            ELSE 0 
        END as kalan_dakika 
        FROM masalar ORDER BY id ASC`;
        
    db.query(sql, (err, results) => {
        if (err) return res.status(500).json(err);
        res.json(results);
    });
});

// MASA AÇ (1 SAATLİK)
app.post('/api/masa-ac', (req, res) => {
    const { id } = req.body;
    const sql = "UPDATE masalar SET durum = 'dolu', baslangic_zamani = NOW() WHERE id = ?";
    db.query(sql, [id], (err, result) => {
        if (err) return res.json(err);
        res.json({ mesaj: "Masa açıldı!" });
    });
});

// MASA KAPAT (HESAP KES)
app.post('/api/masa-kapat', (req, res) => {
    const { id } = req.body;
    const sql = "UPDATE masalar SET durum = 'bos', baslangic_zamani = NULL WHERE id = ?";
    db.query(sql, [id], (err, result) => {
        if (err) return res.json(err);
        res.json({ mesaj: "Masa kapatıldı!" });
    });
});

// YENİ MASA EKLE
app.post('/api/masa-ekle', (req, res) => {
    const { id } = req.body;
    db.query('INSERT INTO masalar (id, durum) VALUES (?, "bos")', [id], (err, result) => {
        if (err) return res.json({ hata: "Hata!" });
        res.json({ mesaj: "Eklendi" });
    });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Admin Panel Port: ${PORT}`));
