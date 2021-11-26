import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'
import { Redirect } from 'react-router-dom'

// Components
import SideNav from '../../components/SideNav/SideNav'
import ProgressIndicator from '../../components/ProgressIndicator/ProgressIndicator'

import Name from './Name/Name'
import Type from './Type/Type'
import Credentials from './Credentials/Credentials'
import Labels from './Labels/Labels'
import Summary from './Summary/Summary'

// CSS
import "./CreateProject.scss"

class CreateProject extends Component {
  constructor(props) {
    super(props)
    this.renderForm = this.renderForm.bind(this)
  }

  renderForm(){
    if (this.props.CreateProjectStore.step === 0){
      return <Name/>
    } else if (this.props.CreateProjectStore.step === 1){
      return <Type/>
    } else if (this.props.CreateProjectStore.step === 2){
      return <Credentials
                needsStorage={this.props.CreateProjectStore.type === "wa" ? 
                false : true}
              />
    } else if (this.props.CreateProjectStore.step === 3){
      return <Labels/>
    } else if (this.props.CreateProjectStore.step === 4){
      return <Summary
                requestCreateProject={this.props.requestCreateProject}
              />
    }
  }

  render() {
    if (!this.props.AppStore.isLoggedIn)
      return <Redirect push to="/login"/>
    return (
      <div>
        <div >
          <SideNav projects={true}/>
        </div>
        <div className="create_project_form">
          <ProgressIndicator
            steps={["Nome", "Tipo", "Credenciais", "Rótulos", "Final"]}
            curStep={this.props.CreateProjectStore.step}
          />
          {this.renderForm()}
        </div>
      </div>
    )
  }
}

CreateProject = inject('CreateProjectStore', 'AppStore')(observer(CreateProject))
export default CreateProject