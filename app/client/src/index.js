import React from "react"
import { render } from "react-dom"
import { BrowserRouter as Router } from "react-router-dom"
import "./index.css"
import "./styles/base.css"
import App from "./App"

render((
    <Router>
        <App />
    </Router>
), document.getElementById('root'))