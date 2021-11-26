import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'
import Button from '../../../components/Button/Button'

//CSS
import "./Summary.scss"

class Summary extends Component {
  render() {
    return (
      <div className="create_project_summary">
        <h3 className="create_project_summary_title">
          Resumo:
        </h3>
        <div className="create_project_summary_item">
          <p>Nome: {this.props.CreateProjectStore.name}</p>
        </div>
        <div className="create_project_summary_item">
          <p>Tipo: {this.props.CreateProjectStore.type}</p>
        </div>
        <div className="create_project_summary_item">
          <p>Api Key: {this.props.CreateProjectStore.api_key}</p>
        </div>
        <div className="create_project_summary_item">
          <p>Url: {this.props.CreateProjectStore.url}</p>
        </div>
        <div className="create_project_summary_buttons create_project_summary_item">
          <Button
            type="primary"
            text="Criar Projeto"
            onClick={this.props.requestCreateProject}
          />
          <div className="create_project_summary_continue">
            <Button
              type="secondary"
              text="Voltar"
              onClick={this.props.CreateProjectStore.prevStep}
            />
          </div>
        </div>
      </div>
    )
  }
}

Summary = inject('CreateProjectStore')(observer(Summary))
export default Summary
