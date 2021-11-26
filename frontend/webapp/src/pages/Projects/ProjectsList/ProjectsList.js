import React, { Component } from 'react'
import { Redirect } from 'react-router-dom'

// Components
import ProjectTile from '../../../components/ProjectTile/ProjectTile'

// CSS
import "./ProjectsList.scss"
export default class ProjectsList extends Component {
  constructor(props) {
    super(props)
    this.goToDashboard = this.goToDashboard.bind(this)
    this.goToLabeling = this.goToLabeling.bind(this)
    this.state = {
      projectDashboard: false,
      sampleLabeling: false,
      selectedProject: null,
    }
  }

  renderProjects(){
    return this.props.projects.map(project => {
      return <ProjectTile
                project={project}
                dashboardCallback={this.goToDashboard}
                labelingCallback={this.goToLabeling}
              />
    })
  }

  goToDashboard(project){
    this.setState({
      projectDashboard: true,
      selectedProject: project
    })
  }

  goToLabeling(project){
    this.setState({
      sampleLabeling: true,
      selectedProject: project
    })
  }

  render() {
    if (this.state.projectDashboard)
      return <Redirect
                push to={{
                          pathname: '/dashboard',
                          state: { project: this.state.selectedProject }
                        }}
              />
    if (this.state.sampleLabeling)
      return <Redirect
                  push to={{
                            pathname: '/labeling',
                            state: { project: this.state.selectedProject }
                          }}
                />
    return (
      this.renderProjects()
    )
  }
}
