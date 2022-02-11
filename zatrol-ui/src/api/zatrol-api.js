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
  console.log(`< GET ${url.toString()} : `, json)
  if (!response.ok) throw new Error(json)
  return json
}

async function post(pathname, body, query) {
  const opts = {
    method: "POST",
    mode: "cors",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  }

  const url = new URL(BASE_URL)
  url.pathname += pathname
  if (query) BASE_URL.search = new URLSearchParams(query)

  console.log(`> POST: ${url.toString()} :`, opts.body.substring(0, 80))
  const response = await fetch(url, opts)
  const json = response.status == 204 ? true : await response.json()
  console.log(`< POST ${url.toString()} : `, json)
  if (!response.ok) throw new Error(json.error)
  return json
}

export async function getRegions() {
  return await get("/metadata/region")
}

export async function getChampions() {
  return await get("/metadata/champion")
}

export async function getSummoners() {
  return await get("/summoner")
}

export async function postSummoner(region, summoner_name) {
  return await post("/summoner", { region, summoner_name })
}

export async function postQuote(puuid, text, champ_restrictions) {
  return await post("/quote", { puuid, text, champ_restrictions })
}
