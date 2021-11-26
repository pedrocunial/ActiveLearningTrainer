import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'
import Button from '../../../components/Button/Button'

//CSS
import "./Summary.scss"

class Summary extends Component {
  render() {
    return (
      <div className="signup_summary">
        <h3 className="signup_summary_title">
          Resumo:
        </h3>
        <div className="signup_summary_item">
          <p>Nome: {this.props.SignUpStore.name}</p>
        </div>
        <div className="signup_summary_item">
          <p>Email: {this.props.SignUpStore.email}</p>
        </div>
        <div className="signup_summary_item">
          <p>Password: {this.props.SignUpStore.password}</p>
        </div>
        <div className="signup_summary_buttons signup_summary_item">
          <Button
            type="primary"
            text="Sign Up"
            onClick={this.props.requestSignUp}
          />
          <div className="signup_summary_continue">
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

Summary = inject('SignUpStore')(observer(Summary))
export default Summary
