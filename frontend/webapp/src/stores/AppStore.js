import { observable, action, computed, decorate } from 'mobx'

class AppStore {
  isLoggedIn = localStorage.getItem('isLoggedIn') || false;
  loginToken = localStorage.getItem('loginToken') || null;
  userId = localStorage.getItem('userId') || null;

  login = (token, userId) => {
    this.isLoggedIn = true;
    localStorage.setItem('isLoggedIn', true)
    this.loginToken = token;
    localStorage.setItem('loginToken', token)
    this.userId = userId
    localStorage.setItem('userId', userId)
  }

  logout = () => {
    this.isLoggedIn = false;
    localStorage.removeItem('isLoggedIn')
    this.loginToken = null;
    localStorage.removeItem('loginToken')
    this.userId = null;
    localStorage.removeItem('userId')
  }

  get getToken() {
    if (this.isLoggedIn)
      return this.loginToken
    else
      return false
  }
}

decorate(AppStore, {
  isLoggedIn: observable,
  loginToken: observable,
  userId: observable,
  login: action,
  logout: action,
  getToken: computed
})


const store = new AppStore();
export default store