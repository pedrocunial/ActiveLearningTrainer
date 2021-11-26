import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'
import "./Type.scss"
import { SelectableTile  } from "carbon-components-react"
import Button from '../../../components/Button/Button'

class Type extends Component {
  constructor(props) {
    super(props)
    this.changeSelectedType = this.changeSelectedType.bind(this)
    this.submitType = this.submitType.bind(this)
    this.state = {
      selectedType: this.props.CreateProjectStore.type,
      text: this.props.CreateProjectStore.type === "text" ? true : false,
      image: this.props.CreateProjectStore.type === "image" ? true : false,
      wa: this.props.CreateProjectStore.type === "wa" ? true : false,
    }
  }

  changeSelectedType(type){
    this.setState({
      selectedType: type,
      text: false,
      image: false,
      wa: false,
      [type]: true
    })
  }

  submitType(){
    if (this.state.selectedType){
      this.props.CreateProjectStore.changeType(this.state.selectedType)
      this.props.CreateProjectStore.nextStep()
    }
  }

  render() {
    return (
      <div className="create_project_types">
        <div className="types">
          <SelectableTile
            value="NLC"
            id="text"
            selected={this.state.text}
            handleClick={() =>  {this.changeSelectedType("text") }}
          >
            <div className="type_content">
              <h3>NLC</h3>
              <img
                src={process.env.PUBLIC_URL + '/project_types/nlc.svg'}
                alt="nlc"
                className="type_image"
              />
            </div>
          </SelectableTile>
          <SelectableTile
            value="WA"
            id="WA"
            className="type"
            selected={this.state.wa}
            handleClick={() =>  {this.changeSelectedType("wa") }}
          >
            <div className="type_content">
              <h3>WA</h3>
              <img
                src={process.env.PUBLIC_URL + '/project_types/wa.png'}
                alt="wa"
                className="type_image"
              />
            </div>
          </SelectableTile>
          <SelectableTile
            value="VR"
            id="image"
            className="type"
            selected={this.state.image}
            handleClick={() =>  {this.changeSelectedType("image") }}
          >
          <div className="type_content">
            <h3>VR</h3>
            <img
              src={process.env.PUBLIC_URL + '/project_types/vr.png'}
              alt="vr"
              className="type_image"
            />
          </div>
          </SelectableTile>
        </div>
        <div className="create_project_types_buttons">
          <Button
            type="primary"
            text="Continuar"
            onClick={this.submitType}
            />
          <div className="create_project_types_continue">
            <Button
              type="secondary"
              text="Voltar"
              onClick={this.props.CreateProjectStore.prevStep}
            />
          </div>
        </div>
      </div>
    )
  }
}

Type = inject('CreateProjectStore')(observer(Type))
export default Type
