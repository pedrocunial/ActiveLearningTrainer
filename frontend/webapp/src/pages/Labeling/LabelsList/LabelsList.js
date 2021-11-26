import React, { Component } from 'react'
import { SelectableTile, Search } from 'carbon-components-react'

// CSS
import "./LabelsList.scss"

export default class LabelsList extends Component {
  constructor(props) {
    super(props)
    this.filterList = this.filterList.bind(this)
    this.state = {
       labels: props.labels,
       search: ""
    }
  }
  
  renderList() {
    return this.state.labels.map(label => {
      return  (
        <SelectableTile
          handleClick={() => this.props.selectLabel(label)}
          selected={this.props.selectedLabel.label === label.label ? true : false}>
          {label.label}
        </SelectableTile>
      )
    })
  }

  componentDidUpdate(oldProps){
    const newProps = this.props
    console.log(newProps, oldProps)
    if (newProps.labels !== oldProps.labels){
      this.setState({
        labels: newProps.labels
      })
    }
  }

  filterList(filter) {
    const fullList = this.props.labels
    const filteredList = fullList.filter(label => {
      return label.label.toLowerCase().includes(filter.toLowerCase())
    })
    this.setState({
      labels: filteredList,
      search: filter
    })
  }

  render() {
    return (
      <div className="full_labels_list">
        <h4>Rótulos</h4>
        <div className="labels_search">
          <Search
            value={this.state.search}
            onChange={(e) => this.filterList(e.target.value)}
          />
        </div>
        <div className="labels_list_labelling">
          {this.renderList()}
        </div>
      </div>
    )
  }
}
