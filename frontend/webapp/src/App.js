import React, { Component } from 'react'
import { BrowserRouter as Router, Route } from "react-router-dom";
import { Provider } from 'mobx-react'

// Components
import Header from './components/Header/Header'

// Pages
import LoginContainer from './pages/Login/LoginContainer'
import ProjectsContainer from './pages/Projects/ProjectsContainer'
import SignUpContainer from './pages/SignUp/SignUpContainer'
import CreateProjectContainer from './pages/CreateProject/CreateProjectContainer'
import LabelingContainer from './pages/Labeling/LabelingContainer'
import ProjectDashboardContainer from './pages/ProjectDashboard/ProjectDashboardContainer'

// Stores
import AppStore from './stores/AppStore'
import SignUpStore from './stores/SignUpStore'
import CreateProjectStore from './stores/CreateProjectStore'

// CSS
import "./App.scss"

const SignUpWithStore = () => {
  return (
    <Provider SignUpStore={SignUpStore}>
      <SignUpContainer />
    </Provider>
  )
}

const CreateProjectWithStore = () => {
  return (
    <Provider CreateProjectStore={CreateProjectStore}>
      <CreateProjectContainer />
    </Provider>
  )
}


export default class App extends Component {
  render() {
    return (
      <div>
        <div className="header">
          <Header color={"blue"}/>
        </div>
        <Provider AppStore={AppStore}>
          <Router>
            <div>
              <Route exact path="/" component={LoginContainer} />
              <Route path="/login" component={LoginContainer} />
              <Route path="/projects" component={ProjectsContainer} />
              <Route path="/signup" component={SignUpWithStore} />
              <Route path="/create_project" component={CreateProjectWithStore} />
              <Route path="/labeling" component={LabelingContainer} />
              <Route path="/dashboard" component={ProjectDashboardContainer} />
            </div>
          </Router>
        </Provider>
      </div>

    )
  }
}
