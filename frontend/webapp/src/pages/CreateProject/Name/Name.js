import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'
import TextInput from '../../../components/TextInput/TextInput'
import Button from '../../../components/Button/Button'
import "./Name.scss"

class Name extends Component {
  constructor(props) {
    super(props)
    this.submitName = this.submitName.bind(this)
    this.state = {
       name: this.props.CreateProjectStore.name,
       invalid: false
    }
  }

  submitName(){
    if (this.state.name){
      this.props.CreateProjectStore.changeName(this.state.name)
      this.props.CreateProjectStore.nextStep()
    } else {
      this.setState({ invalid: true })
    }
  }

  render() {
    return (
      <div>
        <div className="create_project_name">
          <TextInput
            id="project_name"
            label="Nome do Projeto"
            placeholder="Nome"
            invalid = {this.state.invalid}
            invalidText="Nome do projeto não pode estar vazio"
            value={this.state.name}
            onChange={(e) => this.setState({name:e.target.value })}
          />
          <div className="create_project_name_item">
            <Button
              type="primary"
              text="Continuar"
              onClick={this.submitName}
            />
          </div>
        </div>
      </div>
    )
  }
}

Name = inject('CreateProjectStore')(observer(Name))
export default Name
