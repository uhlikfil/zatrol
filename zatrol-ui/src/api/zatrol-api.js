const HOST = process.env.REACT_APP_SERVER_HOST || "http://localhost"
const PORT = process.env.REACT_APP_SERVER_PORT || 8000
const BASE_URL = `${HOST}:${PORT}/api`

async function get(pathname, query) {
  const opts = {
    method: "GET",
    mode: "cors",
    headers: { "Content-Type": "application/json" },
  }

  const url = new URL(BASE_URL)
  url.pathname += pathname
  if (query) BASE_URL.search = new URLSearchParams(query)

  const response = await fetch(url, opts)
  const json = await response.json()
  if (!response.ok) throw new Error(json)
  console.log(`< GET ${url.toString()} : `, json)
  return json
}

export async function getPlayers() {
  return await get("/player")
}
