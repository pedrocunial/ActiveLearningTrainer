import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'
import TextInput from '../../../components/TextInput/TextInput'
import Button from '../../../components/Button/Button'
import "./Password.scss"

class Password extends Component {
  constructor(props) {
    super(props)
    this.state = {
      invalidText: false,
      password: props.SignUpStore.password,
      retypePassword: props.SignUpStore.password
    }
    this.submitPassword = this.submitPassword.bind(this)
  }

  submitPassword(){
    if ((this.state.password !== this.state.retypePassword) || !this.state.password){
      this.setState({
        invalidText: true
      })
    }
    else {
      this.setState({
        invalidText: false
      })
      this.props.SignUpStore.changePassword(this.state.password)
      this.props.SignUpStore.nextStep()
    }
  }

  render() {
    return (
      <div>
        <div className="signup_password">
            <TextInput
              id="signup_password"
              label="Senha"
              placeholder="Senha"
              type="password"
              value={this.state.password}
              onChange={(e) => this.setState({ password: e.target.value })}
            />
          <div className="signup_password_item">
            <TextInput
              id="signup_retype_password"
              label="Confirme Senha"
              placeholder="confirme Senha"
              type="password"
              invalidText="As senhas estão diferentes"
              invalid={this.state.invalidText}
              value={this.state.retypePassword}
              onChange={(e) => this.setState({ retypePassword : e.target.value })}
            />
          </div>
          <div className="signup_password_buttons signup_password_item">
            <Button
              type="primary"
              text="Continuar"
              onClick={this.submitPassword}
            />
            <div className="signup_password_continue">
              <Button
                type="secondary"
                text="Voltar"
                onClick={this.props.SignUpStore.prevStep}
              />
            </div>
          </div>
        </div>
      </div>
    )
  }
}

Password = inject('SignUpStore')(observer(Password))
export default Password