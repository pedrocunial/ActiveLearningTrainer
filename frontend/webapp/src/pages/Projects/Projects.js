import React, { Component } from 'react'
import { Redirect } from 'react-router-dom'
import { inject, observer } from 'mobx-react'

// Components
import Pagination from '../../components/Pagination/Pagination'
import SideNav from '../../components/SideNav/SideNav'
import Button from '../../components/Button/Button'
import ProjectsList from './ProjectsList/ProjectsList'

// CSS
import './Projects.scss'

class Projects extends Component {
  constructor(props) {
    super(props)
    this.getPageProjects = this.getPageProjects.bind(this)
    this.state = {
       createProject: false,
       page: 1,
       projects: []
    }
  }

  getPageProjects(){
    const start = 5 * (this.state.page - 1)
    this.setState({
      projects: this.props.projects.slice(start, start + 5)
    })
  }

  componentDidUpdate(oldProps) {
    const newProps = this.props
    if(oldProps.projects !== newProps.projects) {
      this.getPageProjects()
    }
  }

  render() {
    if (this.state.createProject)
      return <Redirect push to="/create_project"/>
    return (
      <div>
        <div>
          <SideNav projects={true}/>
        </div>
        <div className="title">
          <h1>Projetos</h1>
        </div>
        <div className="pagination">
          <Pagination
            onChange={(e) => this.setState({ page:e.page }, () => { this.getPageProjects()})}
            totalItems={this.props.projects.length}
          />
        </div>
        <div className="projects">
          <ProjectsList
            projects={this.state.projects}
          />
          <div className="create_project">
            <Button
              type="primary"
              text="Criar Projeto"
              onClick={() => this.setState({createProject: true})}
            />
          </div>
        </div>
      </div>
    )
  }
}

Projects = inject('AppStore')(observer(Projects))
export default Projects
