import React, { Component } from 'react'
import { Select as SelectCarbon, SelectItem } from 'carbon-components-react'

// CSS
import "./Select.scss"

export default class Select extends Component {
  constructor(props) {
    super(props)
    this.renderItems = this.renderItems.bind(this)
  }

  renderItems(){
    return this.props.items.map((item) => {
      return <SelectItem
               value={item.value}
               text={item.text}
             />
    })
  }
  render() {
    return (
      <div>
        <SelectCarbon
          labelText={this.props.title}
          onChange={this.props.onChange}
        >
          {this.renderItems()}
        </SelectCarbon>
      </div>
    )
  }
}
