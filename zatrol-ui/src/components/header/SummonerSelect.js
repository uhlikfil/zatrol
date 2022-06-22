import { useQuery } from "@apollo/client"
import { summonersQuery } from "api/zatrol-api"
import chroma from "chroma-js"
import { SummonerContext } from "context/SummonerContext"
import { useContext, useState } from "react"
import Select from "react-select"
import { summonerColor, textColor } from "utils/color-styles"

const SummonerSelect = ({ nameFn }) => {
  const { selectedSummoner, setSelectedSummoner } = useContext(SummonerContext)
  const [summoners, setSummoners] = useState([])
  const { loading, error } = useQuery(summonersQuery, {
    onCompleted: (newData) => {
      const newSummoners = newData.summoners.edges.reduce((sumMap, { node }) => {
        sumMap[node.puuid] = node
        return sumMap
      }, {})
      setSummoners(newSummoners)
    },
  })

  const options = () => {
    if (loading) return []
    if (error) return []
    return Object.values(summoners).map((smnr) => ({
      value: smnr.puuid,
      label: nameFn(smnr),
    }))
  }

  return (
    <Select
      options={options()}
      onChange={(elem) => setSelectedSummoner(summoners[elem.value])}
      width="256px"
      placeholder={loading ? "Loading..." : error ? "Error" : "Select a summoner"}
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
          const color = chroma(summonerColor(selectedSummoner, true))
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
            ":active": {
              backgroundColor: color.hex(),
            },
          }
        },
      }}
    />
  )
}

export default SummonerSelect
