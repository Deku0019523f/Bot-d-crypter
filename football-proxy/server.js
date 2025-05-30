require('dotenv').config(); // Chargement des variables d'environnement

const express = require('express');
const fetch = require('node-fetch');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;
const API_TOKEN = process.env.API_TOKEN;

app.use(cors());

// Route principale du proxy
app.get('/api/:endpoint*', async (req, res) => {
  try {
    const endpoint = req.params.endpoint + (req.params[0] || '');
    if (!endpoint) {
      return res.status(400).json({ error: 'Endpoint requis.' });
    }

    const query = req.url.split('?')[1] || '';
    const url = `https://api.football-data.org/v4/${endpoint}${query ? '?' + query : ''}`;

    console.log(`↔️ Proxying request to: ${url}`);

    const response = await fetch(url, {
      headers: { 'X-Auth-Token': API_TOKEN }
    });

    if (!response.ok) {
      return res.status(response.status).json({ error: `Erreur API: ${response.status}` });
    }

    const data = await response.json();
    res.json(data);

  } catch (err) {
    console.error('❌ Erreur serveur :', err.message);
    res.status(500).json({ error: 'Erreur serveur: ' + err.message });
  }
});

// Test de fonctionnement
app.get('/', (req, res) => {
  res.send('🚀 Proxy Football API opérationnel.');
});

app.listen(PORT, () => {
  console.log(`✅ Proxy en ligne sur http://localhost:${PORT}`);
});
