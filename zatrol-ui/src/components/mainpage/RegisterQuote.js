import { getChampions, postQuote } from "api/zatrol-api"
import chroma from "chroma-js"
import Result from "components/result/Result"
import { SummonerContext } from "context/SummonerContext"
import { useContext, useRef, useState } from "react"
import { useQuery } from "react-query"
import Select from "react-select"
import { summonerColor } from "utils/color-styles"

const RegisterQuote = () => {
  const { summoner } = useContext(SummonerContext)
  const { data: champions, isLoading, isError } = useQuery(["champions"], getChampions)

  const [quoteText, setQuoteText] = useState("")

  const resultRef = useRef()

  const options = () => {
    if (isLoading) return <option>Loading...</option>
    if (isError) return <option>Error loading regions</option>
    return champions.map((champ) => (
      <option key={champ} value={champ}>
        {champ}
      </option>
    ))
  }

  const selectStyles = () => {
    const activeSummonerColor = summonerColor(summoner, true)
    return {
      control: (provided, state) => ({
        ...provided,
        width: state.selectProps.width,
        borderColor: activeSummonerColor,
      }),
      menu: (provided, state) => ({
        ...provided,
        width: state.selectProps.width,
      }),
      option: (provided, state) => {
        const color = chroma(activeSummonerColor)
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
    }
  }

  const submitCallback = async (event) => {
    event.preventDefault()
    if (summoner == null) {
      resultRef.current.error("Select a summoner first!")
      return
    }
    try {
      resultRef.current.loading()
      await postQuote(summoner.puuid, quoteText)
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
              placeholder="whopity scoop"
              value={quoteText}
              onChange={(event) => setQuoteText(event.target.value)}
            />
          </div>
        </div>
        <div className="field">
          <label className="label">Only for specific champions</label>
          <div className="control"></div>
          <Select
            closeMenuOnSelect={false}
            isMulti
            options={options()}
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
