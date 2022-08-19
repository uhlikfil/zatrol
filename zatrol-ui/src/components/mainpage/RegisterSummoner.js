import { faGlobe } from "@fortawesome/free-solid-svg-icons"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { getRegions, postSummoner } from "api/zatrol-api"
import Result from "components/result/Result"
import { SummonerContext } from "context/SummonerContext"
import { useContext, useEffect, useRef, useState } from "react"
import { useQuery, useQueryClient } from "react-query"
import { summonerColor } from "utils/color-styles"

const RegisterSummoner = () => {
  const { summoner } = useContext(SummonerContext)
  const { data: regions, isLoading, isError } = useQuery(["regions"], getRegions)
  useEffect(() => {
    if (!isLoading && !isError) setSelectedRegion(regions[0])
  }, [regions])

  const [selectedRegion, setSelectedRegion] = useState()
  const [summonerName, setSummonerName] = useState("")

  const resultRef = useRef()
  const queryClient = useQueryClient()

  const options = () => {
    if (isLoading) return <option>Loading...</option>
    if (isError) return <option>Error loading regions</option>
    return regions.map((region) => (
      <option key={region} value={region}>
        {region}
      </option>
    ))
  }

  const submitCallback = async (event) => {
    event.preventDefault()
    try {
      resultRef.current.loading()
      await postSummoner(selectedRegion, summonerName)
      resultRef.current.success()
      queryClient.invalidateQueries("summoners")
    } catch (exception) {
      resultRef.current.error(exception)
    }
  }

  return (
    <>
      <form className="container p-6" onSubmit={submitCallback}>
        <div className="field">
          <label className="label">Region</label>
          <div className="control has-icons-left">
            <div className={`select is-fullwidth ${summonerColor(summoner)}`}>
              <select onChange={(event) => setSelectedRegion(event.target.value)}>
                {options()}
              </select>
            </div>
            <div className="icon is-small is-left">
              <FontAwesomeIcon icon={faGlobe} />
            </div>
          </div>
        </div>
        <div className="field">
          <label className="label">Summoner Name</label>
          <div className="control">
            <input
              className={`input ${summonerColor(summoner)}`}
              type="text"
              placeholder="whopity scoop"
              value={summonerName}
              onChange={(event) => setSummonerName(event.target.value)}
            />
          </div>
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

export default RegisterSummoner
