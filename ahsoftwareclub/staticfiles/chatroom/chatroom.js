const roomName = JSON.parse(document.getElementById("room-name").textContent);


const chatSocket = new WebSocket(
    'wss://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

chatSocket.onmessage = function(event){
    const data = JSON.parse(event.data);
    document.getElementById("chat-box").innerHTML += (data.message + '<br/>');
}

document.getElementById('chat-form').focus();

document.getElementById('chat-form').addEventListener('submit', handleChatMessage);

function handleChatMessage(event) {
    // prevent page refresh
    event.preventDefault();
    const messageInputDom = document.getElementById('message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({ 
        'message': message
    }));
    messageInputDom.value = '';
}
