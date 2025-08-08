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
    <label>Provider:
      <select name="provider">
        <option value="gemini">Gemini</option>
        <option value="openai">OpenAI</option>
      </select>
    </label>
    <br/>
    <input type="password" name="api_key" placeholder="API Key" style="width: 420px" required />
    <input type="text" name="target_url" value="https://example.com" style="width: 420px" />
    <select name="model">
      <optgroup label="Gemini">
        <option value="gemini-1.5-flash">gemini-1.5-flash</option>
        <option value="gemini-2.0-flash">gemini-2.0-flash</option>
        <option value="gemini-2.5-flash">gemini-2.5-flash</option>
      </optgroup>
      <optgroup label="OpenAI">
        <option value="gpt-5">gpt-5</option>
        <option value="gpt-4o">gpt-4o</option>
      </optgroup>
    </select>
    <button type="submit">Start</button>
  </form>
</body>
</html>`)
})

app.post('/oneclick-demo', async (req, res) => {
  const { api_key, target_url, model, provider } = req.body
  try {
    const r = await fetch(`${apiBase}/oneclick/start`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ api_key, target_url, model, provider }),
    })
    const text = await r.text()
    let payload
    try { payload = JSON.parse(text) } catch { payload = { raw: text } }
    if (!r.ok) {
      const detail = payload?.detail || payload?.raw || r.statusText || r.status
      return res.status(400).send(`One-click failed: ${detail}`)
    }
    res.set('Content-Type', 'application/json').send(JSON.stringify(payload, null, 2))
  } catch (e) {
    res.status(500).send(`Error contacting API: ${(e && e.message) || e}`)
  }
})

app.listen(PORT, () => {
  console.log(`Frontend health service listening on ${PORT}`)
})