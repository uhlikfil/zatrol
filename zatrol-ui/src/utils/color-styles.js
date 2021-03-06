import { hashStr } from "./hash"

const colors = [
  { bulma: "is-primary", rgb: "#00d1b2" },
  { bulma: "is-link", rgb: "#485fc7" },
  { bulma: "is-info", rgb: "#3e8ed0" },
  { bulma: "is-success", rgb: "#48c78e" },
  { bulma: "is-warning", rgb: "#ffe08a" },
  { bulma: "is-danger", rgb: "#f14668" },
  { bulma: "is-dark", rgb: "#363636" },
]

export const summonerColor = (summoner, asRGB) => {
  if (summoner == null) return asRGB ? "#f5f5f5" : "is-light"
  const idx = hashStr(summoner.puuid) % colors.length
  return asRGB ? colors[idx].rgb : colors[idx].bulma
}

export function textColor(bgColorHex) {
  const c = bgColorHex.substring(1, 7)
  const r = parseInt(c.substring(0, 2), 16) // hexToR
  const g = parseInt(c.substring(2, 4), 16) // hexToG
  const b = parseInt(c.substring(4, 6), 16) // hexToB
  return r * 0.299 + g * 0.587 + b * 0.114 <= 186 ? "#fff" : "#000"
}
