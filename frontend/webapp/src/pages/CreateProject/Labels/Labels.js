import React, { Component } from 'react'
import LabelsList from '../../../components/LabelsList/LabelsList'
import TextInput from '../../../components/TextInput/TextInput'
import Button from '../../../components/Button/Button'
import { inject, observer } from 'mobx-react'

//CSS
import "./Labels.scss"

class Labels extends Component {
  constructor(props) {
    super(props)
    this.addLabel = this.addLabel.bind(this)
    this.submitLabels = this.submitLabels.bind(this)
    this.state = {
       curLabel: ""
    }
  }
  
  addLabel() {
    if (this.state.curLabel){
      this.props.CreateProjectStore.addLabel(this.state.curLabel)
      this.setState({
        curLabel: ""
      })
    }
  }

  submitLabels() {
    if (this.props.CreateProjectStore.labels.length > 0) {
      this.props.CreateProjectStore.nextStep()
    }
  }

  render() {
    if(this.props.CreateProjectStore.type === "wa"){
      this.props.CreateProjectStore.nextStep()
    } return (
      <div className="create_project_labels">
        <TextInput
          id="project_name"
          label="Rótulo"
          placeholder="Rótulo"
          onChange={(e) => this.setState({curLabel: e.target.value})}
          value={this.state.curLabel}
        />
        <div className="create_project_labels_add_label">
          <Button 
            text="Adicionar"
            onClick={this.addLabel}
          />
        </div>
        <div className="create_project_labels_item">
          <p className="create_project_labels_list_title">Rótulos</p>
          <LabelsList
            labels={this.props.CreateProjectStore.labels}
            removeLabel={this.props.CreateProjectStore.removeLabel}
          />
        </div>
        <div className="create_project_labels_buttons create_project_labels_item">
          <Button
            type="primary"
            text="Continuar"
            onClick={this.submitLabels}
          />
          <div className="create_project_labels_continue">
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

Labels = inject('CreateProjectStore')(observer(Labels))
export default Labels
