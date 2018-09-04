import React from 'react'
import axios from 'axios'
import GamesView from './GamesView'

export default class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      players: '',
      games: [],
    }
  }

  handleClick = () => {
    axios.get('/player/view').then((response) => {
      this.setState({
        players: JSON.stringify(response.data),
      })
    }).catch((err) => {
      this.setState({
        players: 'Error: ' + err.response.data,
      })
    })
  }

  handleViewGamesClick = () => {
    axios.get('/game/view').then((response) => {
      this.setState({
        games: response.data,
      })
    }).catch((err) => {
      console.log(err.response)
    })
  }

  handleCreateGameClick = () => {
    axios.post('/game/create').then((response) => {
      alert("created game " + response.data)
    }).catch((err) => {
      alert(err.response.data)
    })
  }

  render() {
    return (<div>
      <button onClick={this.handleClick}>Click me</button>
      <button onClick={this.handleViewGamesClick}>View Games</button>
      <button onClick={this.handleCreateGameClick}>Create Game</button>
      <h5>{this.state.players}</h5>
      <br/>
      <div>
        <GamesView games={this.state.games}/>
      </div>
    </div>)
  }
}
