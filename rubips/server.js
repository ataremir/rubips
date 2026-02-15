const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');
const app = express();

app.use(cors());
app.use(express.json());
app.use(express.static('public'));

const db = mysql.createConnection(process.env.MYSQL_URL);

app.get('/api/masalar', (req, res) => {
  db.query('SELECT * FROM masalar ORDER BY id ASC', (err, results) => {
    if (err) return res.json(err);
    res.json(results);
  });
});

app.post('/api/masa-ekle', (req, res) => {
  const { id } = req.body; 
  db.query('INSERT INTO masalar (id, durum) VALUES (?, "bos")', [id], (err, result) => {
    if (err) return res.json({ hata: "Bu masa numarası zaten var!" });
    res.json({ mesaj: "Yeni masa eklendi!" });
  });
});

app.delete('/api/masa-sil/:id', (req, res) => {
  const id = req.params.id;
  db.query('DELETE FROM masalar WHERE id = ?', [id], (err, result) => {
    if (err) return res.json(err);
    res.json({ mesaj: "Masa silindi!" });
  });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
