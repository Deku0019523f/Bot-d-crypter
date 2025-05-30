require('dotenv').config();
const express = require('express');
const cors = require('cors');
const axios = require('axios');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());

const FOOTBALL_API_BASE_URL = 'https://api.football-data.org/v4';
const API_TOKEN = process.env.FOOTBALL_DATA_API_TOKEN;

// Liste des ID de compétitions à surveiller
const LEAGUE_IDS = [2015, 2021, 2016, 2019, 2002, 2014]; // Ligue 1, Premier League, etc.

// ➤ Proxy /competitions (avec filtre client)
app.get('/competitions', async (req, res) => {
  try {
    const response = await axios.get(`${FOOTBALL_API_BASE_URL}/competitions`, {
      headers: { 'X-Auth-Token': API_TOKEN }
    });

    const filtered = response.data.competitions.filter(comp =>
      LEAGUE_IDS.includes(comp.id)
    );

    res.json({
      count: filtered.length,
      filters: {
        client: 'Bitty alec'
      },
      competitions: filtered
    });
  } catch (error) {
    console.error('Erreur API:', error.message);
    res.status(500).json({ error: 'Erreur lors de l’appel à l’API football-data.org' });
  }
});

// ➤ Route /predictions
app.get('/predictions', async (req, res) => {
  const today = new Date().toISOString().split('T')[0];
  const predictions = [];

  for (const leagueId of LEAGUE_IDS) {
    try {
      const matchRes = await axios.get(`${FOOTBALL_API_BASE_URL}/competitions/${leagueId}/matches`, {
        headers: { 'X-Auth-Token': API_TOKEN },
        params: { dateFrom: today, dateTo: today }
      });

      const matches = matchRes.data.matches;
      if (!matches.length) continue;

      const tableRes = await axios.get(`${FOOTBALL_API_BASE_URL}/competitions/${leagueId}/standings`, {
        headers: { 'X-Auth-Token': API_TOKEN }
      });

      const standings = tableRes.data.standings[0].table;

      for (const match of matches) {
        const home = standings.find(t => t.team.id === match.homeTeam.id);
        const away = standings.find(t => t.team.id === match.awayTeam.id);

        const homeTeam = match.homeTeam.name;
        const awayTeam = match.awayTeam.name;

        const homeRank = home?.position || 10;
        const awayRank = away?.position || 10;

        let score = '1 - 1';
        let winner = 'Égalité';

        if (homeRank < awayRank) {
          score = '2 - 1';
          winner = homeTeam;
        } else if (awayRank < homeRank) {
          score = '1 - 2';
          winner = awayTeam;
        }

        const totalGoals = score.split(' - ').reduce((a, b) => parseInt(a) + parseInt(b), 0);
        const overUnder = totalGoals > 2 ? 'Over 2.5' : 'Under 2.5';

        predictions.push({
          competition: match.competition.name,
          match: `${homeTeam} vs ${awayTeam}`,
          score,
          winner,
          totalGoals,
          overUnder
        });
      }
    } catch (error) {
      console.error(`Erreur pour la ligue ${leagueId}:`, error.message);
    }
  }

  res.json({ predictions });
});

// ➤ Démarrage serveur
app.listen(PORT, () => {
  console.log(`✅ Serveur démarré sur http://localhost:${PORT}`);
});
