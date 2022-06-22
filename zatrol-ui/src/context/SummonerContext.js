import { createContext, useMemo, useState } from "react"

const SummonerContextProvider = ({ children }) => {
  const [selectedSummoner, setSelectedSummoner] = useState(null)
  const value = useMemo(
    () => ({ selectedSummoner, setSelectedSummoner }),
    [selectedSummoner]
  )

  return <SummonerContext.Provider value={value}>{children}</SummonerContext.Provider>
}

export const SummonerContext = createContext({
  selectedSummoner: null,
  setSelectedSummoner: () => {},
})

export default SummonerContextProvider
