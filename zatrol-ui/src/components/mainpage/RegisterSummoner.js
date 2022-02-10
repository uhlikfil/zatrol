import { SummonerContext } from "context/SummonerContext"
import React, { useContext } from "react"

const RegisterSummoner = () => {
  const { summoner, setSummoner } = useContext(SummonerContext)

  return (
    <div className="container p-6">
      <form>
        <div className="field">
          <label className="label">Name</label>
          <div className="control">
            <input className="input" type="text" placeholder="e.g Alex Smith" />
          </div>
        </div>

        <div className="field">
          <label className="label">Email</label>
          <div className="control">
            <input
              className="input"
              type="email"
              placeholder="e.g. alexsmith@gmail.com"
            />
          </div>
        </div>
      </form>
    </div>
  )
}

export default RegisterSummoner
