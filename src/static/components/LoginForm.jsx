import React, {Component} from 'react'
import axios from 'axios'
import {Input,Checkbox, Form} from 'formsy-react-components'
import Formsy from 'formsy-react'

class LoginForm extends Component{
  isValid = () => {
    this.setState({
      valid:true
    });
  }
  isInvalid = () => {
    this.setState({
      valid:false
    });
  }
  submit = (data) => {
    axios.post("/login", data).then( (response) => {
      this.setState({
        message:response.data
      })
    })
  }

  constructor(props){
    super(props)
    this.state= {
      valid:false
    };
  }

  render() {
    return (

      <div>
        <Form
          onValid={this.isValid}
          onInvalid={this.isInvalid}
          onValidSubmit={this.submit}
        >

          <Input name='username' label='username' help='enter your username' validations="maxLength:12" validationError='username too long' required/>
          <Input name='password' type='password' label='password' help='enter your password' validations="minLength:5" validationError='password too short' required/>
          <Checkbox name='remember_me' label='remember me'/>
          <button type='submit' label='login' disabled={!this.state.valid}>Login</button>
        </Form>
        <span>{this.state.message}</span>
      </div>);
  }
}
export default LoginForm;
