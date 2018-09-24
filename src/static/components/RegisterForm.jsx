import React, { Component } from 'react'
import axios from 'axios'
import { withRouter } from 'react-router'


class RegisterForm extends Component {
  isValid = () => {
    this.setState({
      valid: true,
    })
  }
  isInvalid = () => {
    this.setState({
      valid: false,
    })
  }
  submit = (event) => {
    event.preventDefault()
    let data = {username:this.state.username,password:this.state.password}
    axios.post('/register', data, {
      headers: {
        'Content-Type': 'application/json',
      },
    }).then((response) => {
      window.location.replace('/login')
    }).catch((error) => {
      console.log(error.message)
    })
  }

  constructor(props) {
    super(props)
    this.state = {
      username: '',
      password: '',
      passConfirm: '',
      error: {
        usernameError: '',
        passwordError: '',
        passConfirmError: '',
      },
    }
  }

  render() {
    return (
      <div className='container'>
        <div className="jumbotron text-center">
          <h2>
            Register
          </h2>
          <form onSubmit={this.submit}>
            <div className='form-group'>
              <input placeholder='username' className='form-control' type="text" value={this.state.username}
                     onChange={(e) => {
                       this.setState({
                         username: e.target.value,
                       })
                     }}/>
              <small className='form-text text-muted text-danger'>{this.state.error.usernameError}</small>
            </div>

            <div className='form-group'>
              <input placeholder='password' className='form-control' type="password" value={this.state.password}
                     onChange={(e) => {
                       this.setState({
                         password: e.target.value,
                       })
                     }}/>
            </div>

            <div className='form-group'>
              <input placeholder='confirm password' className='form-control' type="password" value={this.state.passConfirm}
                     onChange={(e) => {
                       this.setState({
                         passConfirm: e.target.value,
                       })
                     }}/>
            </div>

            <button className='btn btn-primary' type="submit">
              Register
            </button>
          </form>
        </div>
      </div>)
  }
}

export default RegisterForm
