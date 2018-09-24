import React, { Component } from 'react'
import axios from 'axios'
import { withRouter } from 'react-router'
import '../css/LoginForm.css'

class LoginForm extends Component {

  handlePassChange = (evt) => {
    this.setState({
      password: evt.target.value,
    })
  }

  handleUserChange = (evt) => {
    this.setState({
      username: evt.target.value,
    })
  }

  handleRememberChange = (evt) => {
    this.setState({
      remember_me: evt.target.value,
    })
  }

  submit = (event) => {
    event.preventDefault()
    let data = {
      username: this.state.username, password: this.state.password,
      remember_me: this.state.remember_me,
    }
    axios.post('/login', data).then((response) => {
      console.log(response)
      window.location.replace('/');
    }).catch((error)=>{
      this.setState({
        error:error
      })
    })
  }

  constructor() {
    super()
    this.state = {
      username: '',
      password: '',
      remember_me: false,
      error: '',
    }
  }

  render() {
    return (
      <div className='container'>
        <div className="jumbotron text-center">
          <h2>
            Log In
          </h2>
          <form onSubmit={this.submit}>
            <div className='form-group'>
              <input placeholder='username' className='form-control' type="text" value={this.state.username}
                     onChange={this.handleUserChange}/>
            </div>

            <div className='form-group'>
              <input placeholder='password' className='form-control' type="password" value={this.state.password}
                     onChange={this.handlePassChange}/>
            </div>

            <div className='form-group'>
              <div className='form-check'>
                <input id='remember_me' className='form-check-input' type="checkbox" value={this.state.remember_me}
                       onChange={this.handleRememberChange}/>
                <label htmlFor='remember_me' className='form-check-label'>remember</label>
              </div>
            </div>
            <span className='form-text text-danger'>{this.state.error}</span>
            <button className='btn btn-primary' type="submit" onClick={this.submit}>
              Log In
            </button>
          </form>
        </div>
      </div>)
  }
}

export default LoginForm
