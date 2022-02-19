import { generate } from "api/zatrol-api"
import { SummonerContext } from "context/SummonerContext"
import React, { useContext } from "react"
import { useQuery, useQueryClient } from "react-query"
import { summonerColor } from "utils/color-styles"

const Generate = () => {
  const { summoner } = useContext(SummonerContext)

  const queryClient = useQueryClient()

  const {
    data: imgBase64,
    error,
    isLoading,
    isError,
  } = useQuery(
    ["generate", summoner],
    async () => {
      if (summoner == null) return

      const resp = await generate(summoner.puuid)
      return resp.image
    },
    { staleTime: Infinity, retry: 1 }
  )

  if (summoner == null)
    return (
      <div className="container p-6">
        <div className="notification is-warning">
          Select a Summoner in order to generate Zatrol images
        </div>
      </div>
    )

  if (isLoading)
    return (
      <div className="container my-6">
        <div className="loader-wrapper is-size-1">
          <div className="loader is-loading"></div>
        </div>
      </div>
    )

  if (isError) {
    return (
      <div className="container p-6">
        <div className="notification is-danger">{error.message}</div>
      </div>
    )
  }

  return (
    <div className="columns is-centered p-6">
      <div className="column"></div>
      <div className="column mx-3">
        <div style={{ maxWidth: "800px", margin: "auto" }}>
          <figure className="image">
            <img
              src={`data:image/png;base64,${imgBase64}`}
              alt={`${summoner.summoner_name} memed`}
            />
          </figure>
        </div>
      </div>
      <div className="column">
        <button
          className={`button mb-6 is-large ${summonerColor(summoner)}`}
          onClick={() => queryClient.invalidateQueries("generate")}
        >
          GENERATE NEW
        </button>
      </div>
    </div>
  )
}

export default Generate
