import { observable, action, decorate } from 'mobx'

class CreateProjectStore {
  name = ""
  type = ""
  api_key = ""
  api_key_storage = ""
  instance_id = ""
  workspace_id = ""
  bucket_name = ""
  url = ""
  labels = []
  step = 0

  nextStep = () => {
    this.step += 1
  }

  prevStep = () => {
    this.step -= 1
  }

  changeName = (name) => {
    this.name = name
  }

  changeType = (type) => {
    this.type = type
  }

  changeApiKey = (api_key) => {
    this.api_key = api_key
  }

  changeUrl = (url) => {
    this.url = url
  }

  addLabel = (label) => {
    this.labels.push(label)
  }

  removeLabel = (label) => {
    this.labels = this.labels.filter(item => item !== label)
  }

  changeApiKeyStorage = (api_key) => {
    this.api_key_storage = api_key
  }

  changeInstanceId = (instance_id) => {
    this.instance_id = instance_id
  }

  changeBucketName = (bucket_name) => {
    this.bucket_name = bucket_name
  }

  changeWorkspaceId = (workspace_id) => {
    this.workspace_id = workspace_id
  }
}

decorate(CreateProjectStore, {
  name: observable,
  step: observable,
  api_key: observable,
  api_key_storage: observable,
  instance_id: observable,
  bucket_name: observable,
  url: observable,
  labels: observable,
  workspace_id: observable,
  nextStep: action,
  prevStep: action,
  changeName: action,
  changeType: action,
  changeApiKey: action,
  changeUrl: action,
  changeApiKeyStorage: action,
  changeInstanceId: action,
  changeBucketName: action,
  changeWorkspaceId: action,
  addLabel: action,
  removeLabel: action
})

  
const store = new CreateProjectStore();
export default store