import { getPlayers } from "api/zatrol-api"
import chroma from "chroma-js"
import { SummonerContext } from "context/SummonerContext"
import { useContext } from "react"
import { useQuery } from "react-query"
import Select from "react-select"
import { colors, isDark } from "utils/color-styles"
import { hashStr } from "utils/hash"

const Header = () => {
  const {
    data: players,
    isLoading,
    isError,
  } = useQuery(
    ["players"],
    async () => {
      const playerList = await getPlayers()
      return playerList.reduce((map, p) => {
        map[p.puuid] = p
        return map
      }, {})
    },
    {
      staleTime: 10 * 60 * 1000,
      retryDelay: (attempt) => 2 * (attempt + 1) * 1000,
    }
  )
  const { summoner, setSummoner } = useContext(SummonerContext)

  const name = (summoner) =>
    summoner == null
      ? "Pick a summoner!"
      : `${summoner.summoner_name} #${summoner.region}`

  const summonerColor = (asRGB) => {
    if (summoner == null) return asRGB ? "#f5f5f5" : "is-light"
    const idx = hashStr(summoner.puuid) % colors.length
    if (asRGB) return colors[idx].rgb
    return colors[idx].bulma
  }

  const options = () => {
    if (isLoading) return { value: "loading", label: "Loading..." }
    if (isError) return { value: "error", label: "Error loading players" }
    return Object.values(players).map((p) => {
      return { value: p.puuid, label: name(p) }
    })
  }

  return (
    <section className={`hero is-medium ${summonerColor()}`}>
      <div className="hero-body">
        <p className="title">Zatrol</p>
        <p className="subtitle">{name(summoner)}</p>
        <Select
          options={options()}
          onChange={(elem) => setSummoner(players[elem.value])}
          width="256px"
          styles={{
            control: (provided, state) => ({
              ...provided,
              width: state.selectProps.width,
              border: 0,
              boxShadow: "none",
            }),
            menu: (provided, state) => ({
              ...provided,
              width: state.selectProps.width,
            }),
            option: (provided, state) => {
              const summColor = chroma(summonerColor(true))
              const bgColor = state.isSelected
                ? summColor
                : state.isFocused
                ? summColor.alpha(0.5)
                : chroma("white")
              return {
                ...provided,
                backgroundColor: bgColor.css(),
                color: isDark(bgColor.hex("rgb")) ? "white" : "black",
              }
            },
          }}
        />
      </div>
    </section>
  )
}

export default Header
