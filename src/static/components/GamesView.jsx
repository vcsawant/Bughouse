import React from 'react'
import '../css/GameCardView.css'

class GamesView extends React.Component {
  constructor(props){
    super(props);
  }
  render(){

    var gameList = this.props.games.map((game) => {
      return <GameCard game={game}/>
    })

    return (<table>
      {gameList}
    </table>)
  }
}

class GameCard extends React.Component{

  handleGameJoinClick = (event) => {
    alert('trying to join game: ' + JSON.stringify(this.props.game));
  }

  render(){
    return (<tr style={{width:"100%"}}>
      <div style={{textAlign:'center'}}>
        <h5>{this.props.game.player_white_a}</h5>
        <br/>
        <img style={{width:'50px', height:'50px'}}/>
        <br/>
        <h5>{this.props.game.player_black_a}</h5>
      </div>
      <div style={{textAlign:'center'}}>
        <h5>{this.props.game.player_white_b}</h5>
        <br/>
        <img style={{width:'50px', height:'50px'}}/>
        <br/>
        <h5>{this.props.game.player_black_b}</h5>
      </div>
      <button onClick={this.handleGameJoinClick}>Join Game</button>
    </tr>)
  }
}
export default GamesView;
