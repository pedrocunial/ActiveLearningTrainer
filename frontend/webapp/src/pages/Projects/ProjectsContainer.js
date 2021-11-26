import React, { Component } from 'react'
import { Redirect } from 'react-router-dom'
import { inject, observer } from 'mobx-react'
import Projects from './Projects'
import Notification from '../../components/Notification/Notification'
import URL from '../../utils/url'

class ProjectsContainer extends Component {
  constructor(props) {
    super(props)
    this.requestProjects = this.requestProjects.bind(this)
    this.closeNotification = this.closeNotification.bind(this)
    this.state = {
      loading: true,
      notificaton: false,
      caption: "",
      projects: [],
    }
  }

  closeNotification() {
    this.setState({
      notification: false
    })
  }
  
  requestProjects() {
    const requestParams = {
      method: 'GET',
      headers: {
        "Authorization": 'Token ' + this.props.AppStore.loginToken,
        "Content-Type": "application/json"
      }
    }

    const queryURL = URL.PROJECTS.replace('$uid', this.props.AppStore.userId)

    fetch(queryURL, requestParams)
      .then((response) => {
        if (response.status !== 200)
          throw new Error(response.status)
        return response.json()
      })
      .then((data) => {
        this.setState({projects: data.content, loading: false})
      })
      .catch((e) => this.setState({ notification: true, caption: e.message }))
  }

  componentDidMount(){
    this.requestProjects()
  }


  renderNotification() {
    if (this.state.notification){
      return (
        <Notification
          kind="error"
          title="ERRO"
          subtitle="Ocorreu um erro ao buscar projetos"
          caption={this.state.caption}
          onCloseButtonClick={this.closeNotification}
        />
      )
    }
  }

  render() {
  if (!this.props.AppStore.isLoggedIn)
      return <Redirect push to="/login"/>
    return (
      <div>
        {this.renderNotification()}
        <Projects
          projects={this.state.projects}
        />
      </div>
    )
  }
}

ProjectsContainer = inject('AppStore')(observer(ProjectsContainer))
export default ProjectsContainer
