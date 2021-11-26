import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'
import ProgressIndicator from '../../components/ProgressIndicator/ProgressIndicator'
import InlineLoading from '../../components/InlineLoading/InlineLoading'
import Email from "./Email/Email"
import Password from "./Password/Password"
import Name from './Name/Name'
import Summary from './Summary/Summary'
import "./SignUp.scss"


class SignUp extends Component {
  constructor(props) {
    super(props)
    this.renderForm = this.renderForm.bind(this)
    this.state = {
      loading: props.loading
    }
  }

  componentDidUpdate(oldProps) {
    const newProps = this.props
    if(oldProps.loading !== newProps.loading) {
      if (newProps.loading === true) {
        this.setState({
          loading: newProps.loading
        })
      }
    }
  }

  renderLoading() {
    if (this.state.loading) {
      return (
        <div className="loading_sample">
          <InlineLoading
            success={!this.props.loading}
            description={"Criando Usuário"}
            onSuccess={this.props.goBackToLogin}
          />
        </div>
      )

    }
  }

  renderForm(){
    if (this.props.SignUpStore.step === 0){
      return <Email/>
    } else if (this.props.SignUpStore.step === 1){
      return <Password/>
    } else if (this.props.SignUpStore.step === 2){
      return <Name/>
    } else if (this.props.SignUpStore.step === 3){
      return <Summary requestSignUp={this.props.requestSignUp}/>
    }
  }
  
  render() {
    return (
      <div>
        <div className="form">
          <ProgressIndicator
            steps={["Usuário", "Senha", "Nome", "Final"]}
            curStep={this.props.SignUpStore.step}
          />
          {this.renderForm()}
          {this.renderLoading()}
        </div>
      </div>
    )
  }
}

SignUp = inject('SignUpStore')(observer(SignUp))
export default SignUp
