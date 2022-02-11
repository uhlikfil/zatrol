import React, { forwardRef, useImperativeHandle, useState } from "react"

const STATE = Object.freeze({
  READY: 0,
  LOADING: 1,
  SUCCESS: 2,
  ERROR: 3,
})

const Result = forwardRef((_, ref) => {
  const [state, setState] = useState(STATE.READY)
  const [errorMsg, setErrorMsg] = useState("")

  useImperativeHandle(ref, () => ({
    ready: () => setState(STATE.READY),
    loading: () => setState(STATE.LOADING),
    success: () => {
      setState(STATE.SUCCESS)
      setTimeout(() => setState(STATE.READY), 5000)
    },
    error: (message) => {
      setState(STATE.ERROR)
      setErrorMsg(message)
    },
  }))

  const contents = () => {
    if (state == STATE.LOADING)
      return (
        <div className="loader-wrapper is-size-1">
          <div className="loader is-loading"></div>
        </div>
      )
    return (
      <span className={`tag is-large p-5 ${color()}`}>
        {state == STATE.ERROR ? errorMsg : "SUCCESS!"}
      </span>
    )
  }

  const color = () => {
    switch (state) {
      case STATE.READY:
      case STATE.LOADING:
        return "is-info"
      case STATE.SUCCESS:
        return "is-success"
      case STATE.ERROR:
        return "is-danger"
    }
  }

  if (state == STATE.READY) return null
  return (
    <section className="hero">
      <div className="hero-body has-text-centered">{contents()}</div>
    </section>
  )
})

export default Result
