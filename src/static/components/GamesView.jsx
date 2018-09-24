import React from 'react'
import '../css/GameCardView.css'
import gameSocket from './SocketConnection'

class GamesView extends React.Component {
  constructor(props){
    super(props);
  }
  render(){

    var gameList = this.props.games.map((game) => {
      return <GameCard game={game}/>
    })

    return (<table style={{width:'100%'}}>
      {gameList}
    </table>)
  }
}

class GameCard extends React.Component{

  renderJoinButtonOrPlayerName = function(player, position){

    return (player ? (<h6>{player}</h6>) : (<button onClick={() => {
      let payload = {game_id: this.props.game.id, position: position}
      gameSocket.emit('join', payload)
    }
    }>Join</button>));
  }

  render(){

    return (<tr style={{width:"100%"}}>
      <td style={{textAlign:'center'}}>
        <div>
          {this.renderJoinButtonOrPlayerName(this.props.game.player_white_a,"white_a")}
          <br/>
          <img style={{width:'50px', height:'50px'}}/>
          <br/>
          {this.renderJoinButtonOrPlayerName(this.props.game.player_black_a,"black_a")}
        </div>
      </td>
      <td style={{textAlign:'center'}}>
        <div>
          {this.renderJoinButtonOrPlayerName(this.props.game.player_white_b,"white_b")}
          <br/>
          <img style={{width:'50px', height:'50px'}}/>
          <br/>
          {this.renderJoinButtonOrPlayerName(this.props.game.player_black_b,"black_b")}
        </div>
      </td>
      <td>
        <button onClick={()=>{gameSocket.emit('test');
        console.log('sending test message');
        console.log('connected: ' + gameSocket.connected)}}>Test Socket</button>
      </td>
    </tr>)
  }
}
export default GamesView;
