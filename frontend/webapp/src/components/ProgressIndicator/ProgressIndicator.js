import React, { Component } from 'react'
import { ProgressIndicator as ProgressIndicatorCarbon,
         ProgressStep
       } from 'carbon-components-react'

export default class ProgressIndicator extends Component {
  renderSteps(){
    return (
      this.props.steps.map((step) => {
        return (
          <ProgressStep label={step}/>
        )
      })
    )
  }
  render() {
    return (
      <div>
        <ProgressIndicatorCarbon currentIndex={this.props.curStep}>
          {this.renderSteps()}
        </ProgressIndicatorCarbon>
      </div>
    )
  }
}
