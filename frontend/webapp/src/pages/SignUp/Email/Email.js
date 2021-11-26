import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'
import TextInput from '../../../components/TextInput/TextInput'
import Button from '../../../components/Button/Button'

// CSS
import "./Email.scss"

class Email extends Component {
  constructor(props) {
    super(props)
    this.state = {
      invalidText: false,
      email: props.SignUpStore.email,
      retypeEmail: props.SignUpStore.email
    }
    this.submitEmail = this.submitEmail.bind(this)
  }

  submitEmail(){
    if ((this.state.email !== this.state.retypeEmail) || !this.state.email){
      this.setState({
        invalidText: true
      })
    }
    else {
      this.setState({
        invalidText: false
      })
      this.props.SignUpStore.changeEmail(this.state.email)
      this.props.SignUpStore.nextStep()
    }
  }

  render() {
    return (
      <div className="signup_email">
          <TextInput
            type="email"
            ref="signup_email"
            id="signup_email"
            label="Email"
            placeholder="email"
            value = {this.state.email}
            onChange={(e) => this.setState({ email: e.target.value })}
          />
        <div className="signup_email_item">
          <TextInput
            type="email"
            id="signup_retype_email"
            label="Confirme Email"
            placeholder="email"
            invalidText="Os emails estão diferentes"
            value = {this.state.retypeEmail}
            invalid={this.state.invalidText}
            onChange={(e) => this.setState({ retypeEmail: e.target.value })}
          />
        </div>
        <div className="signup_email_item">
          <Button
            type="primary"
            text="Continuar"
            onClick={this.submitEmail}
          />
        </div>
      </div>
    )
  }
}

Email = inject('SignUpStore')(observer(Email))
export default Email