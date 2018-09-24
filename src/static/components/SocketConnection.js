import io from 'socket.io-client'
const gameSocket = io('/game',{autoConnect:false})

gameSocket.on('connect', () => {
  console.log("connected? " + gameSocket.connected); // true
});

gameSocket.on('status', (data) => {
  console.log(data.message)
})

gameSocket.on('test_response', (data) => {
  console.log(data.sender + " sends " + data.message)
})

export default gameSocket;
