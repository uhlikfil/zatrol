const DEV_HOST = "http://localhost"
const DEV_PORT = 8000
const BASE_URL =
  process.env.NODE_ENV == "production" ? "/api" : `${DEV_HOST}:${DEV_PORT}/api`

async function get(pathname, query, asBinary = false) {
  const opts = {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  }

  let url = BASE_URL + pathname
  if (query) url += "?" + new URLSearchParams(query)

  const response = await fetch(url, opts)
  if (response.status == 500) throw "Unexpected server error!"
  if (!response.ok) throw (await response.json()).detail
  const data = await (asBinary ? response.blob() : response.json())
  console.log(`< GET ${url.toString()} : `, data)
  return data
}

async function post(pathname, body, query) {
  const opts = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  }

  let url = BASE_URL + pathname
  if (query) url += "?" + new URLSearchParams(query)

  console.log(`> POST: ${url.toString()} :`, opts.body.substring(0, 80))
  const response = await fetch(url, opts)
  if (response.status == 500) throw "Unexpected server error!"
  const json = response.status == 204 ? true : await response.json()
  console.log(`< POST ${url.toString()} : `, json)
  if (!response.ok) throw json.detail
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

export async function postSummoner(region, summonerName) {
  return await post("/summoner", { region, summonerName })
}

export async function postQuote(puuid, text, champRestrictions) {
  return await post("/quote", { puuid, text, champRestrictions })
}

export async function generate(puuid) {
  return await get(`/generate/${puuid}`, null, true)
}
