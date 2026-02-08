const roomName = JSON.parse(document.getElementById("room-name").textContent);


const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

chatSocket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    const message = data.message;
    const chatBox = document.getElementById("chat-box");
    const messageElement = document.createElement('div');

    // timestamp stuff
    let time = new Date().toLocaleTimeString();
    const timestamp = document.createElement('div');
    timestamp.className = 'timestamp';
    timestamp.textContent = time;
    messageElement.appendChild(timestamp);

    messageElement.innerHTML += (message['user_name'] + ": " + message['message_text'] + '<br/>');

    chatBox.appendChild(messageElement);
}

document.getElementById('chat-form').focus();

document.getElementById('chat-form').addEventListener('submit', handleChatMessage);

function handleChatMessage(event) {
    // prevent page refresh
    event.preventDefault();
    const messageInputDom = document.getElementById('message-input');
    const message = messageInputDom.value;
    if (message !== '') {
        chatSocket.send(JSON.stringify({
            'message': message
        }));
        messageInputDom.value = '';
    }

}
