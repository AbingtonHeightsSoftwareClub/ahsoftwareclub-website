const roomName = JSON.parse(document.getElementById("room-name").textContent);


const chatSocket = new WebSocket(
    'wss://'
    + window.location.host
    + '/wss/chat/'
    + roomName
    + '/'
);


chatSocket.onmessage = function(event){
    const data = JSON.parse(event.data);
    document.querySelector("#chat-log").value += (data.message + '\n');
}
