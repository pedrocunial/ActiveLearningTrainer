import React, { Component } from 'react'
import { Tile } from 'carbon-components-react'
import Button from '../Button/Button'

// CSS
import "./ProjectTile.scss"

export default class ProjectTile extends Component {
  renderDashboard(){
    if (this.props.project.permission !== 0){
      return (
        <Button
          type="secondary"
          text="Dashboard"
          onClick={() => this.props.dashboardCallback(this.props.project)}
        />
      )
    } else {
      return (
        <div></div>
      )
    }
  }
  render() {
    return (
      <div>
        <Tile className="tile">
          <div className="tile_content">
            <div className="project_title">
              <p className="item">{this.props.project.name}</p>
            </div>
            <div className="project_tile_buttons">
              {this.renderDashboard()}
              <div className="project_tile_button">
                <Button
                  type="secondary"
                  text="Rotular"
                  onClick={() => this.props.labelingCallback(this.props.project)}
                />
              </div>
            </div>
          </div>
        </Tile>
      </div>
    )
  }
}
