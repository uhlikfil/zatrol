import { getSummoners } from "api/zatrol-api"
import chroma from "chroma-js"
import { SummonerContext } from "context/SummonerContext"
import { useContext } from "react"
import { useQuery } from "react-query"
import Select from "react-select"
import { summonerColor, textColor } from "utils/color-styles"

const SummonerSelect = ({ nameFn }) => {
  const { summoner, setSummoner } = useContext(SummonerContext)
  const {
    data: summoners,
    isLoading,
    isError,
  } = useQuery(
    ["summoners"],
    async () => {
      const summonerList = await getSummoners()
      return summonerList.reduce((map, p) => {
        map[p.puuid] = p
        return map
      }, {})
    },
    {
      staleTime: 10 * 60 * 1000,
      retry: 3,
    }
  )

  const options = () => {
    if (isLoading) return [{ value: "loading", label: "Loading..." }]
    if (isError) return [{ value: "error", label: "Error loading summoners" }]
    return Object.values(summoners).map((p) => {
      return { value: p.puuid, label: nameFn(p) }
    })
  }

  const selectCallback = (elem) => {
    if (elem.value == "error" || elem.value == "loading") return
    setSummoner(summoners[elem.value])
  }

  return (
    <Select
      options={options()}
      onChange={selectCallback}
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
          const color = chroma(summonerColor(summoner, true))
          const bgColor = (
            state.isSelected
              ? color
              : state.isFocused
              ? color.alpha(0.5)
              : chroma("white")
          ).hex()
          return {
            ...provided,
            backgroundColor: bgColor,
            color: textColor(bgColor),
          }
        },
      }}
    />
  )
}

export default SummonerSelect
