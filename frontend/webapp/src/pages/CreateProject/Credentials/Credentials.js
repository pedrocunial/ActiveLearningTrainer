import React, { Component } from 'react'
import { inject, observer } from 'mobx-react'
import TextInput from '../../../components/TextInput/TextInput'
import Button from '../../../components/Button/Button'

//CSS
import "./Credentials.scss"

class Credentials extends Component {
  constructor(props) {
    super(props)
    this.submitCredentials = this.submitCredentials.bind(this)
    this.renderStorageCredentials = this.renderStorageCredentials.bind(this)
    this.renderWorkspaceId = this.renderWorkspaceId.bind(this)
    this.state = {
       // Text Input Values
       api_key: props.CreateProjectStore.api_key,
       api_key_storage: props.CreateProjectStore.api_key_storage,
       url: props.CreateProjectStore.url,
       instance_id: props.CreateProjectStore.instance_id,
       bucket_name: props.CreateProjectStore.bucket_name,
       workspace_id: props.CreateProjectStore.workspace_id,
       // Invalid Text Inputs
       workspace_id_invalid: false,
       api_key_storage_invalid: false,
       instance_id_invalid: false,
       bucket_name_invalid: false,
       api_key_invalid: false,
       url_invalid: false
    }
  }

  submitCredentials() {
    if (
      (this.state.api_key &&  this.state.url) 
      && (
        (
          this.state.api_key_storage 
          && this.state.instance_id 
          && this.state.bucket_name
        ) 
        || (
          !this.props.needsStorage
          && this.state.workspace_id
        )
      )
    ) {
      this.props.CreateProjectStore.changeApiKey(this.state.api_key)
      this.props.CreateProjectStore.changeUrl(this.state.url)
      this.props.CreateProjectStore.changeApiKeyStorage(this.state.api_key_storage)
      this.props.CreateProjectStore.changeInstanceId(this.state.instance_id)
      this.props.CreateProjectStore.changeBucketName(this.state.bucket_name)
      this.props.CreateProjectStore.changeWorkspaceId(this.state.workspace_id)
      this.props.CreateProjectStore.nextStep()
    } else {
      this.setState({
                      api_key_invalid: this.state.api_key ? false : true,
                      url_invalid: this.state.url ? false : true,
                      api_key_storage_invalid: this.state.api_key_storage ? false: true,
                      instance_id_invalid: this.state.instance_id ? false : true,
                      bucket_name_invalid: this.state.bucket_name ? false : true,
                      workspace_id_invalid: this.state.workspace_id ? false : true
                    })
    }
  }

  renderWorkspaceId() {
    if (!this.props.needsStorage) {
      return (
        <div className="create_project_credentials_item">
          <TextInput
            id="create_project_workspace_id"
            label="Workspace ID"
            placeholder="Workspace ID"
            invalid = {this.state.workspace_id_invalid}
            value={this.state.workspace_id}
            invalidText="Workspace ID não pode estar vazio"
            onChange={(e) => this.setState({ workspace_id: e.target.value })}
          />
        </div>
      )
    }
  }
  
  renderStorageCredentials() {
    if (this.props.needsStorage) {
      return (
        <div className="create_project_credentials_item">
          <h3> Object Storage </h3>
          <div className="create_project_credentials_item">
            <TextInput
              id="create_project_storage_api_key"
              label="Api Key Storage"
              placeholder="Api Key Storage"
              invalid = {this.state.api_key_storage_invalid}
              value={this.state.api_key_storage}
              invalidText="Api Key Storage não pode estar vazio"
              onChange={(e) => this.setState({ api_key_storage: e.target.value })}
            />
          </div>
          <div className="create_project_credentials_item">
            <TextInput
              id="create_project_instance_id"
              label="Instance ID"
              placeholder="Instance ID"
              invalid = {this.state.instance_id_invalid}
              value={this.state.instance_id}
              invalidText="Instance ID não pode estar vazio"
              onChange={(e) => this.setState({ instance_id: e.target.value })}
            />
          </div>
          <div className="create_project_credentials_item">
            <TextInput
              id="create_project_bucket_name"
              label="Bucket Name"
              placeholder="Bucket Name"
              invalid = {this.state.bucket_name_invalid}
              value={this.state.bucket_name}
              invalidText="Bucket Name não pode estar vazio"
              onChange={(e) => this.setState({ bucket_name: e.target.value })}
            />
          </div>
        </div>
      )
    }
  }

  render() {
    return (
      <div className="create_project_credentials">
        <h3> Classificador </h3>
        <div className="create_project_credentials_item">
          <TextInput
            id="create_project_api_key"
            label="Api Key"
            placeholder="Api Key"
            invalid = {this.state.api_key_invalid}
            value={this.state.api_key}
            invalidText="Api Key não pode estar vazio"
            onChange={(e) => this.setState({ api_key: e.target.value })}
          />
        </div>
        <div className="create_project_credentials_item">
          <TextInput
            id="create_project_api_url"
            label="Url"
            placeholder="Url"
            invalid = {this.state.url_invalid}
            invalidText="Url não pode estar vazio"
            value={this.state.url}
            onChange={(e) => this.setState({ url : e.target.value })}
          />
        </div>
        {this.renderWorkspaceId()}
        {this.renderStorageCredentials()}
        <div className="create_project_credentials_buttons create_project_credentials_item">
          <Button
            type="primary"
            text="Continuar"
            onClick={this.submitCredentials}
          />
          <div className="create_project_credentials_continue">
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

Credentials = inject('CreateProjectStore')(observer(Credentials))
export default Credentials

