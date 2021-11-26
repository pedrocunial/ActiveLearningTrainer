import React, { Component } from 'react'
import { InlineNotification as InlineNotificationCarbon} from 'carbon-components-react'

export default class InlineNotification extends Component {
  render() {
    return (
      <div>
        <InlineNotificationCarbon
            kind={this.props.kind}
            title={this.props.title}
            subtitle={this.props.subtitle}
            onCloseButtonClick={this.props.onCloseButtonClick}
        />
      </div>
    )
  }
}
