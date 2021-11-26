import React, { Component } from 'react'
import { Redirect } from 'react-router-dom'
import { inject, observer } from 'mobx-react' 
import SignUp from './SignUp'
import URL from '../../utils/url'

class SignUpContainer extends Component {
  constructor(props) {
    super(props)
    this.requestSignUp = this.requestSignUp.bind(this)
    this.goBackToLogin = this.goBackToLogin.bind(this)
    this.state = {
      userCreated: false,
      loading: false
    }
  }

  goBackToLogin() {
    this.setState({
      userCreated: true
    })
  }

  requestSignUp() {
    this.setState({
      loading: true
    })

    const body = {
      username: this.props.SignUpStore.email,
      password: this.props.SignUpStore.password,
      name: this.props.SignUpStore.name
    }

    const requestParams = {
      method: 'POST',
      body: JSON.stringify(body),
      headers: {
        "Content-Type": "application/json"
      }
    }
    
    fetch(URL.SIGN_UP, requestParams)
      .then((response) => {
        if (response.status !== 201)
          throw new Error(response.status)
        return response.json()
      })
      .then((data) => {
        this.setState({ loading: false })
      })
      .catch((e) => console.log(e.message))
  }

  render() {
    if (this.state.userCreated) {
      return (
        <Redirect push to="/login"/>
      )
    } return (
      <div>
        <SignUp
          requestSignUp={this.requestSignUp}
          loading={this.state.loading}
          goBackToLogin={this.goBackToLogin}
        />
      </div>
    )
  }
}

SignUpContainer = inject('SignUpStore')(observer(SignUpContainer))
export default SignUpContainer
