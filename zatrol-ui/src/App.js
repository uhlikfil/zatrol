import { QueryClient, QueryClientProvider } from "react-query"
import Header from "./components/header/Header"
import SummonerContextProvider from "./context/SummonerContext"

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      staleTime: 10,
    },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <SummonerContextProvider>
        <Header />
      </SummonerContextProvider>
    </QueryClientProvider>
  )
}

export default App
