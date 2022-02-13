import { getChampions, postQuote } from "api/zatrol-api"
import chroma from "chroma-js"
import Result from "components/result/Result"
import { SummonerContext } from "context/SummonerContext"
import { useContext, useRef, useState } from "react"
import { useQuery } from "react-query"
import Select from "react-select"
import { summonerColor, textColor } from "utils/color-styles"

const RegisterQuote = () => {
  const { summoner } = useContext(SummonerContext)
  const { data: champions, isLoading, isError } = useQuery(["champions"], getChampions)

  const [quoteText, setQuoteText] = useState("")
  const [selectedChampions, setSelectedChampions] = useState([])

  const resultRef = useRef()

  const selectStyles = () => {
    let activeSummonerColor = chroma(summonerColor(summoner, true))
    const activeSummonerColorLight = activeSummonerColor.alpha(0.3).hex()
    activeSummonerColor = activeSummonerColor.hex()
    return {
      control: (provided, state) => ({
        ...provided,
        width: "100%",
        borderColor: activeSummonerColor,
        boxShadow: state.isFocused ? `0 0 0 2px ${activeSummonerColorLight}` : "none",
        ":hover": {
          borderColor: activeSummonerColor,
        },
      }),
      dropdownIndicator: (provided) => ({ ...provided, color: activeSummonerColor }),
      indicatorSeparator: (provided) => ({ ...provided, color: activeSummonerColor }),
      clearIndicator: (provided) => ({ ...provided, color: activeSummonerColor }),
      menu: (provided) => ({
        ...provided,
        width: "100%",
      }),
      option: (provided, state) => {
        const bgColor = state.isFocused ? activeSummonerColorLight : "white"
        return {
          ...provided,
          backgroundColor: bgColor,
          color: textColor(bgColor),
          ":active": {
            backgroundColor: activeSummonerColor,
          },
        }
      },
      multiValue: (provided) => ({
        ...provided,
        backgroundColor: activeSummonerColorLight,
      }),
      multiValueLabel: (provided) => ({
        ...provided,
        color: textColor(activeSummonerColorLight),
      }),
      multiValueRemove: (provided) => ({
        ...provided,
        color: activeSummonerColor,
        ":hover": {
          backgroundColor: activeSummonerColor,
          color: "white",
        },
      }),
    }
  }

  const options = () => {
    if (isLoading) return []
    if (isError) return []
    return champions.map((champ) => ({ value: champ, label: champ }))
  }

  const selectCallback = (state) => {
    const selectedChampionNames = state.map((item) => item.value)
    setSelectedChampions(selectedChampionNames)
  }

  const submitCallback = async (event) => {
    event.preventDefault()
    if (summoner == null) {
      resultRef.current.error("Select a summoner first!")
      return
    }
    try {
      resultRef.current.loading()
      await postQuote(summoner.puuid, quoteText, selectedChampions)
      resultRef.current.success()
    } catch (exception) {
      resultRef.current.error(exception.message)
    }
  }

  return (
    <>
      <form className="container p-6" onSubmit={submitCallback}>
        <div className="field">
          <label className="label">Quote Text</label>
          <div className="control">
            <input
              className={`input ${summonerColor(summoner)}`}
              type="text"
              placeholder={
                summoner == null
                  ? "Select a summoner first"
                  : `${summoner.summoner_name} always says...`
              }
              value={quoteText}
              onChange={(event) => setQuoteText(event.target.value)}
            />
          </div>
        </div>
        <div className="field">
          <label className="label">Only for specific champions</label>
          <div className="control"></div>
          <Select
            options={options()}
            onChange={selectCallback}
            placeholder={
              isLoading ? "Loading..." : isError ? "Error" : "Select champions"
            }
            isMulti
            closeMenuOnSelect={false}
            styles={selectStyles()}
          />
        </div>
        <div className="field">
          <div className="control">
            <button className={`button is-fullwidth ${summonerColor(summoner)}`}>
              Submit
            </button>
          </div>
        </div>
      </form>
      <Result ref={resultRef} />
    </>
  )
}

export default RegisterQuote
