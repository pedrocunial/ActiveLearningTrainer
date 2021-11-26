import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'
import SideNav from '../../components/SideNav/SideNav'
import Button from '../../components/Button/Button'
import InlineNotification from '../../components/InlineNotification/InlineNotification'
import Image from './Image/Image'
import Text from './Text/Text'
import Modal from './Modal/Modal'
import LabelsList from './LabelsList/LabelsList'
import InlineLoading from '../../components/InlineLoading/InlineLoading'

// CSS
import './Labeling.scss'

class Labeling extends Component {
  constructor(props) {
    super(props)
    this.selectLabel = this.selectLabel.bind(this)
    this.renderSample = this.renderSample.bind(this)
    this.renderLoading = this.renderLoading.bind(this)
    this.renderSelectedLabel = this.renderSelectedLabel.bind(this)
    this.addNewLabel = this.addNewLabel.bind(this)
    this.checkContainsLabel = this.checkContainsLabel.bind(this)
    this.sendLabeledSample = this.sendLabeledSample.bind(this)
    this.renderNoLabelError = this.renderNoLabelError.bind(this)
    this.state = {
      noLabelError: false,
      labels: props.sample.labels,
      selectedLabel: {label: null, id: null},
      loading: props.loading,
      openModal: false
    }
  }

  selectLabel(label) {
    this.setState({
      selectedLabel: label,
      noLabelError: false
    })
  }

  renderSample() {
    if (this.props.sample.type === "image") {
      return <Image
                url={this.props.sample.content}
              />
    } else if (this.props.sample.type === "text"
               || this.props.sample.type === "wa") {
      return <Text
                text={this.props.sample.content}
              />
    }
  } 

  checkContainsLabel(label){
    return this.props.sample.labels
            .filter(e => e.label === label).length > 0
  }

  addNewLabel(label) {
    const newLabel = {
      id: -1,
      label: label.trim()
    }

    if (!this.checkContainsLabel(label)){
      this.setState({
        labels: [...this.state.labels, newLabel],
        openModal: false
      })
      this.selectLabel(newLabel)
    }
  }

  renderLoading() {
    if (this.state.loading) {
      return (
        <div className="loading_sample">
          <InlineLoading
            success={!this.props.loading}
            description={"Enviando amostra"}
            onSuccess={() => this.setState({ loading: false })}
          />
        </div>
      )
    }
  }

  renderSelectedLabel() {
    if (this.state.selectedLabel.label !== null) {
      return <p className="label_text">{this.state.selectedLabel.label}</p>
    } return <p className="label_text">Selecione um rótulo</p>
  }

  componentDidUpdate(oldProps) {
    const newProps = this.props
    if(oldProps.loading !== newProps.loading) {
      if (newProps.loading === true) {
        this.setState({
          loading: newProps.loading
        })
      }
    } if (oldProps.sample !== newProps.sample) {
      this.setState({
        labels: newProps.sample.labels,
        selectedLabel: {label: null, id: null},
      })
    }
  }

  sendLabeledSample() {
    if (this.state.selectedLabel.id === null){
      this.setState({
        noLabelError: true
      })
    } else {
      this.props.sendLabeledSample(this.state.selectedLabel)
    }
  }

  renderNoLabelError() {
    if (this.state.noLabelError)
      return (
        <InlineNotification
          kind="error"
          title="Erro"
          subtitle="Nenhum rótulo selecionado"
          onCloseButtonClick={() => this.setState({ noLabelError: false })}
        />
      )
  }

  render() {
    return (
      <div>
        <div>
          <SideNav
            projects={true}
          />
        </div>
        <div className="title">
          <h1>{this.props.project.name}</h1>
        </div>
        <div className="label_list">
          <LabelsList
            labels={this.state.labels}
            selectLabel={this.selectLabel}
            selectedLabel={this.state.selectedLabel}
          />
          <div className="add_label_button">
            <Button
              type="secondary"
              text="Adicionar Rótulo"
              onClick={() => this.setState({ openModal: true })}
            />
          </div>
        </div>
        <div className="sample">
          {this.renderSample()}
            <div className="sample_item send_labeled_sample">
              {this.renderSelectedLabel()}
              <div className="send_labeled_sample_button">
                <Button
                  type="primary"
                  text="Enviar"
                  onClick={this.sendLabeledSample}
                />
              </div>
            </div>
            {this.renderNoLabelError()}
          {this.renderLoading()}
        </div>
        <div>
           <Modal
              open={this.state.openModal}
              primaryButtonText="Adicionar Rótulo"
              secondaryButtonText="Voltar"
              onRequestClose={() => { this.setState({ openModal: false })} }
              submit={this.addNewLabel}
           />
        </div>
      </div>
    )
  }
}

Labeling = inject('AppStore')(observer(Labeling))
export default Labeling
