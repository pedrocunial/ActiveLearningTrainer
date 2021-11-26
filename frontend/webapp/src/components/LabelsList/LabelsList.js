import React, { Component } from 'react'
import { Tile } from 'carbon-components-react'
import Button from '../Button/Button'

//CSS
import "./LabelsList.scss"

export default class LabelsList extends Component {
  constructor(props) {
    super(props)
    this.renderLabelsList = this.renderLabelsList.bind(this)
  }

  renderLabel(label) {
    return (
      <div>
        <Tile className="label_name">
          <div>
            {label}
          </div>
          <Button 
            type="secondary"
            text={"Remover"}
            onClick={() => this.props.removeLabel(label)}
          />
        </Tile>
      </div>
    )
  }

  renderLabelsList() {
    return this.props.labels.map(label => {
      return this.renderLabel(label)
    })
  }

  render() {
    return (
      <div className="labels_list">
        {this.renderLabelsList()}
      </div>
    )
  }
}
