import express from 'express'

const app = express()
const PORT = process.env.PORT || 5173

app.get('/health', (_req, res) => {
  res.json({ status: 'ok', service: 'frontend' })
})

app.get('/', (_req, res) => {
  res.send('<html><body><h1>Dashboard placeholder</h1><p>React + Tailwind scaffold coming soon.</p></body></html>')
})

app.listen(PORT, () => {
  console.log(`Frontend health service listening on ${PORT}`)
})