import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'
import { Redirect } from 'react-router-dom'
import ProjectDashboard from './ProjectDashboard'
import URL from '../../utils/url'

class ProjectDashboardContainer extends Component {
  constructor(props) {
    super(props)
    this.requestProjectMembers = this.requestProjectMembers.bind(this)
    this.requestProjectDetails = this.requestProjectDetails.bind(this)
    this.requestProjectAccuracy = this.requestProjectAccuracy.bind(this)
    this.requestAddMember = this.requestAddMember.bind(this)
    this.state = {
       accuracy: 0,
       project: {
         name: props.location.state.project.name,
         data_count: 0,
         labelled_count: 0
       },
       members: []
    }
  }

  requestAddMember(username, permission) {
    const body = {
      user: {
        username,
        permission: parseInt(permission)
      }
    }
    const requestParams = {
      method: 'POST',
      body: JSON.stringify(body),
      headers: {
        "Authorization": 'Token ' + this.props.AppStore.loginToken,
        "Content-Type": "application/json"
      }
    }

    const queryURL = URL.ADD_USER.replace('$pid', this.props.location.state.project.id)

    fetch(queryURL, requestParams)
      .then((response) => {
        if (response.status !== 201)
          throw new Error(response.status)
        return response.json()
      })
      .then((data) => {
        this.requestProjectMembers()
      })
      .catch((e) => console.log(e.message))
  }

  requestProjectDetails() {
    const requestParams = {
      method: 'GET',
      headers: {
        "Authorization": 'Token ' + this.props.AppStore.loginToken,
        "Content-Type": "application/json"
      }
    }

    const queryURL = URL.PROJECT.replace('$pid', this.props.location.state.project.id)

    fetch(queryURL, requestParams)
      .then((response) => {
        if (response.status !== 200)
          throw new Error(response.status)
        return response.json()
      })
      .then((data) => {
        this.setState({
          project: {
            name:this.props.location.state.project.name,
            data_count: data.content.data_count,
            labelled_count: data.content.labelled_count
          }
        })
      })
      .catch((e) => console.log(e.message))
  }
  
  requestProjectAccuracy() {
    const requestParams = {
      method: 'GET',
      headers: {
        "Authorization": 'Token ' + this.props.AppStore.loginToken,
        "Content-Type": "application/json"
      }
    }

    fetch((URL.ACCURACY + "?project=" + this.props.location.state.project.id),
           requestParams)
      .then((response) => {
        if (response.status !== 200)
          throw new Error(response.status)
        return response.json()
      })
      .then((data) => {
        this.setState({
          accuracy: data.project.accuracy * 100
        })
      })
      .catch((e) => console.log(e.message))
  }

  requestProjectMembers() {
    const requestParams = {
      method: 'GET',
      headers: {
        "Authorization": 'Token ' + this.props.AppStore.loginToken,
        "Content-Type": "application/json"
      }
    }

    const queryURL = URL.USERS.replace('$pid', this.props.location.state.project.id)

    fetch(queryURL, requestParams)
      .then((response) => {
        if (response.status !== 200)
          throw new Error(response.status)
        return response.json()
      })
      .then((data) => {
        this.setState({
          members: data.content
        })
      })
      .catch((e) => console.log(e.message))
  }

  componentWillMount(){
    this.requestProjectMembers()
    this.requestProjectDetails()
    this.requestProjectAccuracy()
  }

  render() {
    if (!this.props.AppStore.isLoggedIn)
      return <Redirect push to="/login"/>
    return (
      <div>
        <ProjectDashboard
          requestAddMember={this.requestAddMember}
          project={this.state.project}
          accuracy={this.state.accuracy}
          members={this.state.members}
        />
      </div>
    )
  }
}

ProjectDashboardContainer = inject('AppStore')(observer(ProjectDashboardContainer))
export default ProjectDashboardContainer