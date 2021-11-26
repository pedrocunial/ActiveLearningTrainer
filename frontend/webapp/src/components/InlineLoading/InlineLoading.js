import React, { Component } from 'react'
import { InlineLoading as InlineLoadingCarbon } from 'carbon-components-react'

// CSS
import "./InlineLoading.scss"
export default class InlineLoading extends Component {
  render() {
    return (
      <div>
        <InlineLoadingCarbon
            success={this.props.success}
            description={this.props.description}
            onSuccess={this.props.onSuccess}
        />
      </div>
    )
  }
}
