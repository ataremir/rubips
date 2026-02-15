const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');
const app = express();

app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// --- BÖLÜM 1: VERÝTABANI BAÐLANTISI ---
// Railway'deki "Variables" kýsmýndaki bilgileri buraya baðlayacaðýz
const db = mysql.createConnection(process.env.MYSQL_URL || {
  host: 'BURAYA_HOST_GELECEK',
  user: 'BURAYA_USER_GELECEK',
  password: 'BURAYA_PASSWORD_GELECEK',
  database: 'BURAYA_DATABASE_GELECEK',
  port: 3306
});

// --- BÖLÜM 2: MASA YÖNETÝMÝ (SENÝN ÝSTEDÝÐÝN KISIM) ---

// Satýr 30: Tüm Masalarý Listele
app.get('/api/masalar', (req, res) => {
  db.query('SELECT * FROM masalar ORDER BY id ASC', (err, results) => {
    if (err) return res.json(err);
    res.json(results);
  });
});

// Satýr 38: Yeni Masa Ekle (Dinamik)
app.post('/api/masa-ekle', (req, res) => {
  const { id } = req.body; 
  db.query('INSERT INTO masalar (id, durum) VALUES (?, "bos")', [id], (err, result) => {
    if (err) return res.json({ hata: "Bu masa numarasý zaten var!" });
    res.json({ mesaj: "Yeni masa eklendi!" });
  });
});

// Satýr 46: Masayý Sil (Dinamik)
app.delete('/api/masa-sil/:id', (req, res) => {
  const id = req.params.id;
  db.query('DELETE FROM masalar WHERE id = ?', [id], (err, result) => {
    if (err) return res.json(err);
    res.json({ mesaj: "Masa dükkandan kaldýrýldý!" });
  });
});

// --- BÖLÜM 3: SUNUCUYU BAÞLAT ---
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Sistem ${PORT} portunda çalýþýyor...`);
});