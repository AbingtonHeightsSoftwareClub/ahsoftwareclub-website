const roomName = JSON.parse(document.getElementById("room-name").textContent);


const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

chatSocket.onopen = function (event) {
    const data = JSON.parse(event.data);
    const payload = data.message;

    const usernameList = payload['active_users'];
    const userIDs = payload['active_user_ids'];
    for (let i = 0; i < userIDs.length; i++) {
        if (document.getElementById(userIDs[i]) == null) {
            const userElement = document.createElement('div');
            userElement.id = userIDs[i];
            userElement.innerHTML = usernameList[i];
        }
    }
}

chatSocket.onmessage = function (event) {
    console.log(event)
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

    const usernameList = message['active_users'];
    const userIDs = message['active_user_ids'];
    for (let i = 0; i < userIDs.length; i++) {
        if (document.getElementById(userIDs[i]) == null) {
            const userElement = document.createElement('span');
            userElement.id = userIDs[i];
            userElement.innerHTML = usernameList[i];
            document.getElementById('user-count').appendChild(userElement);
        }
    }
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
