import React, { Component } from 'react'
import { Modal as ModalCarbon } from 'carbon-components-react'
import TextInput from '../../../components/TextInput/TextInput'
import Select from '../../../components/Select/Select'

// CSS
import "./Modal.scss"

const PERMISSIONS = [
  {
    value: 0,
    text: "Rotulador"
  },
  {
    value: 1,
    text: "Admin"
  }
]

export default class Modal extends Component {
  constructor(props) {
    super(props)
    this.state = {
       username: "",
       selectedPermission: 0 
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
        onRequestSubmit={() => this.props.submit(this.state.username, 
                                                 this.state.selectedPermission)}
        onSecondarySubmit={this.props.onRequestClose}
      >
        <div>
          <TextInput
            label="Email Usuário"
            placeholder="Email Usuário"
            value={this.state.username}
            onChange={(e) => this.setState({ username: e.target.value })}
            dark
          />
          <div className="modal_body_item">
            <Select
              title="Permissão"
              items={PERMISSIONS}
              onChange={(e) => this.setState({selectedPermission: e.target.value})}
            />
          </div>
        </div>

      </ModalCarbon>
    )
  }
}
