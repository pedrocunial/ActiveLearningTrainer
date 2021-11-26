import React, { Component } from 'react'
import { inject, observer } from 'mobx-react' 
import Notification from '../../components/Notification/Notification'
import Login from './Login'
import URL from '../../utils/url'

class LoginContainer extends Component {
  constructor(props) {
    super(props)
    this.requestLogin = this.requestLogin.bind(this)
    this.closeNotification = this.closeNotification.bind(this)
    this.renderNotification = this.renderNotification.bind(this)
    this.state = {
      notification: false,
      caption: ""
    }
  }

  closeNotification() {
    this.setState({
      notification: false
    })
  }
  
  requestLogin(username, password) {
    const body = {
      username,
      password
    }

    const requestParams = {
      method: 'POST',
      body: JSON.stringify(body),
      headers: {
        "Content-Type": "application/json"
      }
    }
    
    fetch(URL.LOGIN, requestParams)
      .then((response) => {
        if (response.status !== 200)
          throw new Error(response.status)
        return response.json()
      })
      .then((data) => {
        this.props.AppStore.login(data.token, data.uid)
      })
      .catch((e) => this.setState({ notification: true, caption: e.message }))
  }

  renderNotification() {
    if (this.state.notification){
      return (
        <Notification
          kind="error"
          title="ERRO"
          subtitle="Ocorreu um erro ao fazer login"
          caption={this.state.caption}
          onCloseButtonClick={this.closeNotification}
        />
      )
    }
  }

  render() {
    return (
      <div>
        {this.renderNotification()}
        <Login
          requestLogin={this.requestLogin}
        />
      </div>
    )
  }
}

LoginContainer = inject('AppStore')(observer(LoginContainer))
export default LoginContainer;
