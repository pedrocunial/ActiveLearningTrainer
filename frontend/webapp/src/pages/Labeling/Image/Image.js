import React, { Component } from 'react'
import "./Image.scss"

export default class Image extends Component {
  render() {
    return (
      <img src={this.props.url} alt="sample" className="image_sample"/>
    )
  }
}
