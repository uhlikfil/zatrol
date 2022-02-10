import { createContext, useMemo, useState } from "react"

const SummonerContextProvider = ({ children }) => {
  const [summoner, setSummoner] = useState(null)
  const value = useMemo(() => ({ summoner, setSummoner }), [summoner])

  return <SummonerContext.Provider value={value}>{children}</SummonerContext.Provider>
}

export const SummonerContext = createContext({
  summoner: null,
  setSummoner: () => {},
})

export default SummonerContextProvider
