import React, { Component } from 'react'
import { ToastNotification } from 'carbon-components-react'
import "./Notification.scss"

export default class Notification extends Component {
  render() {
    return (
        <ToastNotification
            kind={this.props.kind}
            title={this.props.title}
            subtitle={this.props.subtitle}
            onCloseButtonClick={this.props.onCloseButtonClick}
            caption={this.props.caption}
            className="notification"
        />
    )
  }
}
