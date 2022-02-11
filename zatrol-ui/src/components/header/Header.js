import { SummonerContext } from "context/SummonerContext"
import { useContext } from "react"
import { Link, matchPath, useLocation } from "react-router-dom"
import { summonerColor } from "utils/color-styles"
import SummonerSelect from "./SummonerSelect"

const Header = () => {
  const { summoner } = useContext(SummonerContext)
  const currentUrl = useLocation()

  const isActive = (pattern) => {
    return matchPath(pattern, currentUrl.pathname) != null
  }

  const name = (summoner) =>
    summoner == null
      ? "Pick a summoner!"
      : `${summoner.summoner_name} #${summoner.region}`

  return (
    <section className={`hero ${summonerColor(summoner)}`}>
      <div className="hero-body">
        <p className="title">
          <Link to={"/"}>Zatrol</Link>
        </p>
        <p className="subtitle">{name(summoner)}</p>
        <SummonerSelect nameFn={name} />
      </div>
      <div className="hero-foot">
        <nav className="tabs is-boxed is-fullwidth">
          <div className="container">
            <ul>
              <li
                className={isActive("/generate/*") || isActive("/") ? "is-active" : ""}
              >
                <Link to="/generate">Generate Image</Link>
              </li>
              <li className={isActive("/regquote/*") ? "is-active" : ""}>
                <Link to="regquote">Register Quotes</Link>
              </li>
              <li className={isActive("/regsumm/*") ? "is-active" : ""}>
                <Link to="/regsumm">Register Summoner</Link>
              </li>
            </ul>
          </div>
        </nav>
      </div>
    </section>
  )
}

export default Header
