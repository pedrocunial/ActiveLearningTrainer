import React, { Component } from 'react'
import { Redirect } from 'react-router-dom'
import { inject, observer } from 'mobx-react'
import CreateProject from './CreateProject' 
import URL from '../../utils/url'

class CreateProjectContainer extends Component {
  constructor(props) {
    super(props)
    this.requestCreateProject = this.requestCreateProject.bind(this)
    this.state = {
      projectCreated: false
    }
  }
  
  requestCreateProject() {
    const body = {
      name: this.props.CreateProjectStore.name,
      type: this.props.CreateProjectStore.type,
      user_id: this.props.AppStore.userId,
      classifier_credentials: {
        api_key: this.props.CreateProjectStore.api_key,
        url: this.props.CreateProjectStore.url,
        workspace_id: this.props.CreateProjectStore.workspace_id
      },
      storage_credentials: {
        api_key_storage: this.props.CreateProjectStore.api_key_storage,
         instance_id: this.props.CreateProjectStore.instance_id,
         bucket_name: this.props.CreateProjectStore.bucket_name
      },
      labels: this.props.CreateProjectStore.labels
    }

    const requestParams = {
      method: 'POST',
      body: JSON.stringify(body),
      headers: {
        "Authorization": 'Token ' + this.props.AppStore.loginToken,
        "Content-Type": "application/json"
      }
    }
    
    fetch(URL.CREATE_PROJECT, requestParams)
      .then((response) => {
        if (response.status !== 201)
          throw new Error(response.status)
        return response.json()
      })
      .then((data) => {
        this.setState({ projectCreated: true })
      })
      .catch((e) => console.log(e.message))
  }

  render() {
    if (!this.props.AppStore.isLoggedIn)
      return <Redirect push to="/login"/>
    if (this.state.projectCreated)
      return <Redirect push to="/projects"/>
    return (
      <div>
        <CreateProject
          requestCreateProject={this.requestCreateProject}
        />
      </div>
    )
  }
}

CreateProjectContainer = inject('CreateProjectStore', 'AppStore')(observer(CreateProjectContainer))
export default CreateProjectContainer