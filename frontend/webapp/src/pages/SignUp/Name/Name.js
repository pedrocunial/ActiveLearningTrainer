import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'
import TextInput from '../../../components/TextInput/TextInput'
import Button from '../../../components/Button/Button'

// CSS
import "./Name.scss"

class Name extends Component {
  constructor(props) {
    super(props)
    this.submitEmail = this.submitEmail.bind(this)
    this.state = {
       name: props.SignUpStore.name
    }
  }

  submitEmail(){
    this.props.SignUpStore.changeName(this.state.name)
    this.props.SignUpStore.nextStep()
  }
  
  render() {
    return (
      <div className="signup_name">
        <TextInput
          id="signup_name"
          label="Nome Completo"
          placeholder="nome"
          value = {this.state.name}
          onChange={(e) => this.setState({ name: e.target.value })}
        />
        <div className="signup_name_buttons signup_name_item">
          <Button
            type="primary"
            text="Continuar"
            onClick={this.submitEmail}
          />
          <div className="signup_name_continue">
            <Button
              type="secondary"
              text="Voltar"
              onClick={this.props.SignUpStore.prevStep}
            />
          </div>
        </div>
      </div>
    )
  }
}

Name = inject('SignUpStore')(observer(Name))
export default Name