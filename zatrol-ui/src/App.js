import Header from "components/header/Header"
import Generate from "components/mainpage/Generate"
import RegisterQuote from "components/mainpage/RegisterQuote"
import RegisterSummoner from "components/mainpage/RegisterSummoner"
import SummonerContextProvider from "context/SummonerContext"
import { QueryClient, QueryClientProvider } from "react-query"
import { useRoutes } from "react-router-dom"

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      staleTime: 10 * 60 * 1000,
      retry: 3,
    },
  },
})

const RoutedViews = () =>
  useRoutes([
    { path: "/", element: <Generate /> },
    { path: "/generate", element: <Generate /> },
    { path: "/quote", element: <RegisterQuote /> },
    { path: "/summoner", element: <RegisterSummoner /> },
  ])

const App = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <SummonerContextProvider>
        <Header />
        <RoutedViews />
      </SummonerContextProvider>
    </QueryClientProvider>
  )
}

export default App
