let url =  `ws://${window.location.host}/ws/socket-server/`

const chatSocket = new WebSocket(url)

chatSocket.onmessage = function(e) {
    
}
