const express = require('express');
const fetch = require('node-fetch');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

const API_TOKEN = '73e80cc8f9c44d9db3243ffcd652f508';

app.use(cors());

app.get('/api/:endpoint*', async (req, res) => {
  try {
    const endpoint = req.params.endpoint + (req.params[0] || ''); // pour gérer les sous-chemins comme /competitions/FL1/matches
    const query = req.url.split('?')[1] || '';
    const url = `https://api.football-data.org/v4/${endpoint}${query ? '?' + query : ''}`;

    const response = await fetch(url, {
      headers: { 'X-Auth-Token': API_TOKEN }
    });

    if (!response.ok) {
      return res.status(response.status).json({ error: `Erreur API: ${response.status}` });
    }

    const data = await response.json();
    res.json(data);

  } catch (err) {
    res.status(500).json({ error: 'Erreur serveur: ' + err.message });
  }
});

app.get('/', (req, res) => {
  res.send('🚀 Proxy Football API opérationnel.');
});

app.listen(PORT, () => {
  console.log(`✅ Proxy en ligne sur http://localhost:${PORT}`);
});
