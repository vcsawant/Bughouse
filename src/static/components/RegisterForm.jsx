import React, {Component} from 'react'
import axios from 'axios'
import {Input, Form} from 'formsy-react-components'
import {addValidationRule} from 'formsy-react'

addValidationRule('isUnique', function (values, username) {
  return axios.get('/player/view/'+username).then( (response) => {
    return false;
  }).catch( (error) => {
    return true;
  })
});

class RegisterForm extends Component{
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
    this.setState({
      message:JSON.stringify(data)
    });
    axios.post('/register', data, {
      headers: {
        'Content-Type': 'application/json'
      }}).then( (response) => {
      this.setState({
        message:response.data.toString()
      }).catch( (error) => {
        console.log(error.message)
      })
    });
  }

  constructor(props){
    super(props)
    this.state= {
      valid:false,
      message:""
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

          <Input name='username' label='username' help='enter your username' validations="isUnique" validationErrors="username exists" required/>
          <Input name='password' type='password' label='password' help='enter your password' validations="minLength:5" validationError='password too short' required/>
          <Input name='pass_confirm' type='password' label='confirm password' help='confirm your password' validations='equalsField:password' validationError='password does not match' required/>
          <button type='submit' disabled={!this.state.valid}>Login</button>

          {/* debugging purposes */}
          <span>{this.state.message}</span>
        </Form>
      </div>);
  }
}
export default RegisterForm;
