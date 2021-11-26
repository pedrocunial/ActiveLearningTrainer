import React, { Component } from 'react'
import { TextInput as TextInputCarbon } from 'carbon-components-react'
import './TextInput.scss'

export default class TextInput extends Component {
  render() {
    return (
      <div>
        <TextInputCarbon
          id={this.props.id}
          labelText={this.props.label}
          placeholder={this.props.placeholder}
          type={this.props.type}
          invalid={this.props.invalid}
          invalidText={this.props.invalidText}
          value={this.props.value}
          onChange={this.props.onChange}
          light={!this.props.dark}
        />
      </div>
    )
  }
}
