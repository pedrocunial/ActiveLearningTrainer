import React, { Component } from 'react'
import {Button as ButtonCarbon} from 'carbon-components-react'
import './Button.scss'

export default class Button extends Component {
  render() {
    return (
      <div>
        <ButtonCarbon 
          kind={this.props.type}
          onClick={this.props.onClick}
          >
          {this.props.text}
        </ButtonCarbon>
      </div>
    )
  }
}
