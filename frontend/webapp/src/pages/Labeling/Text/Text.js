import React, { Component } from 'react'
import { TextArea } from 'carbon-components-react' 
import './Text.scss'

export default class Text extends Component {
  render() {
    return (
      <div>
        <TextArea
          className="text"
          labelText="Amostra"
          value={this.props.text}
          placeholder="Placeholder text."
          disabled
          light
          id="test2"
        />
      </div>
    )
  }
}
