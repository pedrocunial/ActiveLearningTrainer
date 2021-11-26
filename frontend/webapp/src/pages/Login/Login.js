import React, { Component } from 'react';
import { Redirect } from 'react-router-dom'
import './Login.scss';
import TextInput from '../../components/TextInput/TextInput'
import Button from '../../components/Button/Button'
import { inject, observer } from 'mobx-react' 

class Login extends Component {
  constructor(props) {
    super(props)
    this.state = {
       signUp: false,
       username: "",
       password: ""
    }
  }

  render() {
    if (this.state.signUp) {
      return <Redirect push to="/signup"/>
    } if (this.props.AppStore.isLoggedIn) {
      return <Redirect push to="/projects"/>
    }
    return (
      <div className="body">
        <div className="form">
          <TextInput 
            id="username"
            label="Username"
            placeholder="username"
            value={this.state.username}
            onChange={(e) => this.setState({ username:e.target.value })}
          />
          <div className="password">
            <TextInput 
              id="password"
              label="Password"
              placeholder="password"
              type="password"
              value={this.state.password}
              onChange={(e) => this.setState({ password:e.target.value })}
            />
            <div className="buttons">
              <Button
                type="primary"
                text="Login"
                onClick={() => this.props.requestLogin(this.state.username, this.state.password)}
              />
              <div className="signup">
                <Button
                  type="secondary"
                  text="Sign Up"
                  onClick={() => this.setState({signUp: true})}
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

Login = inject('AppStore')(observer(Login))
export default Login;
