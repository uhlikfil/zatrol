import { ApolloClient, ApolloProvider, InMemoryCache } from "@apollo/client"
import Header from "components/header/Header"
import Generate from "components/mainpage/Generate"
import RegisterQuote from "components/mainpage/RegisterQuote"
import RegisterSummoner from "components/mainpage/RegisterSummoner"
import SummonerContextProvider from "context/SummonerContext"
import { QueryClient, QueryClientProvider } from "react-query"
import { useRoutes } from "react-router-dom"
import { BASE_URL } from "./api/zatrol-api"

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      staleTime: 10 * 60 * 1000,
      retry: 3,
    },
  },
})

const gqlClient = new ApolloClient({
  uri: BASE_URL + "/graphql",
  cache: new InMemoryCache(),
})

const RoutedViews = () =>
  useRoutes([
    { path: "/", element: <Generate /> },
    { path: "/generate", element: <Generate /> },
    { path: "/regquote", element: <RegisterQuote /> },
    { path: "/regsumm", element: <RegisterSummoner /> },
  ])

const App = () => {
  return (
    <ApolloProvider client={gqlClient}>
      <QueryClientProvider client={queryClient}>
        <SummonerContextProvider>
          <Header />
          <RoutedViews />
        </SummonerContextProvider>
      </QueryClientProvider>
    </ApolloProvider>
  )
}

export default App
