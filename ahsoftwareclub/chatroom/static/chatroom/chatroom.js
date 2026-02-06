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
    document.getElementById("chat-box").textContent += (data.message + '\n');
}

document.getElementById('chat-form').focus();
document.getElementById('chat-form').onkeyup = function(e) {
    if (e.key === 'Enter') {  // enter, return
        document.getElementById('send-button').click();
    }
};

document.getElementById('send-button').onclick = function(e) {
    // prevent page refresh
    e.preventDefault();
    const messageInputDom = document.getElementById('chat-form').elements['message-input'];
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({ 
        'message': message
    }));
    messageInputDom.value = '';
};
