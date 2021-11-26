import React, { Component } from 'react'
import { Modal as ModalCarbon } from 'carbon-components-react'
import TextInput from '../../../components/TextInput/TextInput'

// CSS
import "./Modal.scss"

export default class Modal extends Component {
  constructor(props) {
    super(props)
    this.state = {
       newLabel: "",
    }
  }
  
  render() {
    return (
      <ModalCarbon
        open={this.props.open}
        modalHeading={this.props.title}
        primaryButtonText={this.props.primaryButtonText}
        secondaryButtonText={this.props.secondaryButtonText}
        onRequestClose={this.props.onRequestClose}
        onRequestSubmit={() => this.props.submit(this.state.newLabel)}
        onSecondarySubmit={this.props.onRequestClose}
      >
        <div>
          <TextInput
            label="Novo Rótulo"
            placeholder="Novo Rótulo"
            value={this.state.newLabel}
            onChange={(e) => this.setState({ newLabel: e.target.value })}
            dark
          />
        </div>

      </ModalCarbon>
    )
  }
}
