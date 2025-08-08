import express from 'express'

const app = express()
const PORT = process.env.PORT || 5173

app.use(express.urlencoded({ extended: true }))
app.use(express.json())

const apiBase = process.env.API_BASE || 'http://localhost:8000/api/v1'

app.get('/health', (_req, res) => {
  res.json({ status: 'ok', service: 'frontend' })
})

app.get('/', (_req, res) => {
  res.send(`<!doctype html>
<html>
<head><title>Security Testing Dashboard</title></head>
<body>
  <h1>One-Click LLM Scan</h1>
  <form method="post" action="/oneclick-demo">
    <input type="password" name="api_key" placeholder="Gemini API Key" style="width: 320px" required />
    <input type="text" name="target_url" value="https://example.com" style="width: 420px" />
    <select name="model">
      <option value="gemini-1.5-flash">gemini-1.5-flash</option>
      <option value="gemini-2.0-flash">gemini-2.0-flash</option>
      <option value="gemini-2.5-flash">gemini-2.5-flash</option>
    </select>
    <button type="submit">Start</button>
  </form>
</body>
</html>`)
})

app.post('/oneclick-demo', async (req, res) => {
  const { api_key, target_url, model } = req.body
  try {
    const r = await fetch(`${apiBase}/oneclick/start`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ api_key, target_url, model }),
    })
    const j = await r.json()
    if (!r.ok) {
      return res.status(400).send(`One-click failed: ${j.detail || r.status}`)
    }
    res.set('Content-Type', 'application/json').send(JSON.stringify(j, null, 2))
  } catch (e) {
    res.status(500).send('Error contacting API')
  }
})

app.listen(PORT, () => {
  console.log(`Frontend health service listening on ${PORT}`)
})