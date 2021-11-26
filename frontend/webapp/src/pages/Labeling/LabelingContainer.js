import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'
import { Redirect } from 'react-router-dom'
import Labeling from './Labeling'
import URL from '../../utils/url'

class LabelingContainer extends Component {
  constructor(props) {
    super(props)
    this.requestSample = this.requestSample.bind(this)
    this.sendLabeledSample = this.sendLabeledSample.bind(this)
    this.state = {
      loading: false,
      sample: {
        type: null,
        labels: []
      }
    }
  }

  sendLabeledSample(label) {
    this.setState({
      loading: true,
    })

    const body = {
      id: this.state.sample.id,
      label: {
        label: label.label,
        id: label.id,
        is_new: false
      }
    }
    const requestParams = {
      method: 'POST',
      body: JSON.stringify(body),
      headers: {
        "Authorization": 'Token ' + this.props.AppStore.loginToken,
        "Content-Type": "application/json"
      }
    }

    fetch((URL.CLASSIFY + "?project=" + this.props.location.state.project.id),
           requestParams)
      .then((response) => {
        if (response.status !== 200)
          throw new Error(response.status)
        return response.json()
      })
      .then((data) => {
        this.requestSample()
      })
      .catch((e) => console.log(e.message))
  }

  requestSample() {
    const requestParams = {
      method: 'GET',
      headers: {
        "Authorization": 'Token ' + this.props.AppStore.loginToken,
        "Content-Type": "application/json"
      }
    }
    
    fetch((URL.CLASSIFY + "?project=" + this.props.location.state.project.id),
           requestParams)
      .then((response) => {
        if (response.status !== 200)
          throw new Error(response.status)
        return response.json()
      })
      .then((data) => {
        this.setState({
          loading: false,
          sample: data
        })
      })
      .catch((e) => console.log(e.message))
  }

  componentWillMount(){
    this.requestSample()
  }

  render() {
    if (!this.props.AppStore.isLoggedIn)
      return <Redirect push to="/login"/>
    return (
      <div>
        <Labeling
          loading={this.state.loading}
          project={this.props.location.state.project}
          sendLabeledSample={this.sendLabeledSample}
          sample={this.state.sample}
        />
      </div>
    )
  }
}

LabelingContainer = inject('AppStore')(observer(LabelingContainer))
export default LabelingContainer