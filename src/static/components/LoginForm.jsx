import React, {Component} from 'react'
import axios from 'axios'
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import RaisedButton from 'material-ui/RaisedButton'
import TextField from 'material-ui/TextField';
import Checkbox from 'material-ui/Checkbox';
import Paper from 'material-ui/Paper'

class LoginForm extends Component{
  constructor(props){
    super(props)
    this.state= {
      valid:false
    };
  }

  isValid(){
    this.setState({
      valid:true
    });
  }

  isInvalid(){
    this.setState({
      valid:false
    });
  }

  submit = (data) => {
    alert(JSON.stringify(data, null, 4));
  }

  render() {
    return (
      <Paper>
        <Formsy.Form
          onValid={this.isValid}
          onInvalid={this.isInvalid}
          onValidSubmit={this.submit}
        >
        </Formsy.Form>
        <TextField id='username' label='username' validations="isAlphanumeric"/>
        <TextField id='password' label='password' validations='minLength:5'/>
        <Checkbox name='remember_me' label='remember me'/>
        <RaisedButton type='submit' label='login' disabled={this.state.valid}/>
      </Paper>);
  }
}
export default LoginForm;