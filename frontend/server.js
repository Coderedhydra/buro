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
  <h1>Enter Gemini API Key</h1>
  <form method="post" action="/set-key">
    <input type="password" name="api_key" placeholder="Gemini API Key" style="width: 320px" required />
    <button type="submit">Save</button>
  </form>
  <h2>Plan Safe Tests (demo)</h2>
  <form method="post" action="/plan-demo">
    <input type="text" name="url" value="https://example.com/api/items" style="width: 420px" />
    <select name="method">
      <option>GET</option>
      <option>POST</option>
    </select>
    <button type="submit">Plan</button>
  </form>
  <h2>Generate Probe Requests (demo)</h2>
  <form method="post" action="/generate-demo">
    <input type="text" name="url" value="https://example.com/api/items" style="width: 420px" />
    <select name="method">
      <option>GET</option>
      <option>POST</option>
    </select>
    <textarea name="plan" placeholder='Paste plan JSON here' rows="8" cols="80"></textarea>
    <button type="submit">Generate</button>
  </form>
</body>
</html>`)
})

app.post('/set-key', async (req, res) => {
  const { api_key } = req.body
  try {
    const r = await fetch(`${apiBase}/config/llm/gemini-key`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ api_key }),
    })
    if (!r.ok) {
      const j = await r.json().catch(() => ({}))
      return res.status(400).send(`Failed to set key: ${j.detail || r.status}`)
    }
    res.redirect('/')
  } catch (e) {
    res.status(500).send('Error contacting API')
  }
})

app.post('/plan-demo', async (req, res) => {
  const { url, method } = req.body
  try {
    const r = await fetch(`${apiBase}/planner/plan`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url, method, params: [{ name: 'q', location: 'query' }] }),
    })
    const j = await r.json()
    if (!r.ok) {
      return res.status(400).send(`Plan failed: ${j.detail || r.status}`)
    }
    res.set('Content-Type', 'application/json').send(JSON.stringify(j, null, 2))
  } catch (e) {
    res.status(500).send('Error contacting API')
  }
})

app.post('/generate-demo', async (req, res) => {
  const { url, method, plan } = req.body
  try {
    const planObj = JSON.parse(plan)
    const r = await fetch(`${apiBase}/probe/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url, method, params: [{ name: 'q', location: 'query' }], plan: planObj }),
    })
    const j = await r.json()
    if (!r.ok) {
      return res.status(400).send(`Generate failed: ${j.detail || r.status}`)
    }
    res.set('Content-Type', 'application/json').send(JSON.stringify(j, null, 2))
  } catch (e) {
    res.status(400).send('Invalid plan JSON or API error')
  }
})

app.listen(PORT, () => {
  console.log(`Frontend health service listening on ${PORT}`)
})