import { observable, action, decorate } from 'mobx'

class SignUpStore {
  name = ""
  email = ""
  password = ""
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

  changePassword = (password) => {
    this.password = password
  }

  changeEmail = (email) => {
    this.email = email
  }

}

decorate(SignUpStore, {
  name: observable,
  email: observable,
  step: observable,
  nextStep: action,
  prevStep: action,
  changeName: action,
  changePassword: action,
  changeEmail: action
})

  
const store = new SignUpStore();
export default store