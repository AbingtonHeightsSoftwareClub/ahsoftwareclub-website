const roomName = JSON.parse(document.getElementById("room-name").textContent);


let connection = "";

/*
* https = http secure
* wss = ws secure = websocket secure
*
* There are two types of get requests with normal webservers: http and https
* http is insecure while https uses a secure signed certificate to be secure
*
* Websockets act like that too. To create a websocket connection, the client needs to make an http or https request
* to the server. Once connected, it needs to ask to upgrade its connection to a websocket connection. An http connection
* can only be upgraded to a ws connection, and an https connection can only be upgraded to a wss connection.
*
* When developing, we use a self-hosted development server. So, we can only make http requests without a lot of configuration.
* But, in production, we need to use https for security and so browsers don't block our website.
* Hence, we need to check if we are using http (development) or https (production) to determine if we must use ws or wss.
*  */

if (location.protocol === "https:") {
    connection = 'wss://'
        + window.location.host
        + '/ws/chat/'
        + roomName
        + '/'
} else {
    connection = 'ws://'
        + window.location.host
        + '/ws/chat/'
        + roomName
        + '/'
}

const chatSocket = new WebSocket(connection)
const chatBox = document.getElementById("chat-box");
chatSocket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    console.log(data)
    switch (data.type) {
        case "chat_message":
            handle_chat_message(data)
            break;
        case "chat_file":
            handle_chat_file(data);
            break;
        case "chat_connect":
            handle_connection(data);
            break;
        case "chat_disconnect":
            handle_disconnection(data);
            break;
    }
    const chatBox = document.getElementById('chat-box');
    chatBox.scrollTop = chatBox.scrollHeight;
}

const chatForm = document.getElementById("message-input");
chatForm.focus();
chatForm.onkeyup = function (e) {
    if (e.key === 'Enter') {  // enter, return
        chatSocket.send(JSON.stringify({"type": "message", "message": chatForm.value}));
        chatForm.value = "";
        chatForm.focus();
    }
};

// stolen from stackoverflow lmao oops
const fileInput = document.getElementById('file-input')
fileInput.addEventListener('change', function (event) {
    const file = event.target.files[0];
    toDataURL(file, function (dataURL) {
        chatSocket.send(JSON.stringify({
            "type": "file",
            "dataURL": dataURL
        }))
    })
});

function handle_chat_message(data) {
    const message = data.message;
    const username = data.username;
    let message_div = document.createElement("div");

    let last_node = chatBox.lastChild;
    if (last_node.firstChild != null) {
        console.log(last_node.className);
        if (last_node.firstChild.className !== username) {
            let username_span = document.createElement("span");

            username_span.textContent = username;
            username_span.classList.add(username);

            username_span.classList.add("username");
            add_timestamp(message_div);
            message_div.appendChild(username_span);
        }

    } else {
        let username_span = document.createElement("span");
        username_span.textContent = username;
        username_span.classList.add(username);

        username_span.classList.add("username");
        add_timestamp(message_div);
        message_div.appendChild(username_span);

    }
    let message_span = document.createElement("span");
    message_span.innerHTML = message;
    message_span.className = username;
    message_div.appendChild(message_span);

    chatBox.appendChild(message_div);
}

function handle_chat_file(data) {
    const dataURL = data.dataURL;
    const username = data.username;
    let image = document.createElement('img');
    image.src = dataURL;
    let username_span = document.createElement('span');
    username_span.textContent = username;
    username_span.classList.add(username);
    username_span.classList.add("username");
    let message_div = document.createElement('div');
    add_timestamp(message_div);
    message_div.appendChild(username_span);
    message_div.appendChild(image);

    chatBox.appendChild(message_div);
}

function handle_connection(data) {
    const userBox = document.getElementById('user-count')
    const activeUsers = data.activeUsers;
    const activeUserIDs = data.activeUserIDs;

    for (let i = 0; i < activeUsers.length; i++) {
        if (document.getElementById(activeUserIDs[i]) == null) {
            const userElement = document.createElement("div");
            userElement.textContent += activeUsers[i];
            userElement.id = activeUserIDs[i];
            userBox.appendChild(userElement);
        }
    }
}

function handle_disconnection(data) {
    if (document.getElementById(data.userID) !== null) {
        document.getElementById(data.userID).remove()
    }
}

function add_timestamp(element) {
    // timestamp stuff
    let time = new Date().toLocaleTimeString();
    const timestamp = document.createElement('div');
    timestamp.className = 'timestamp';
    timestamp.textContent = time;
    element.appendChild(timestamp);
}

// stolen from a stackoverflow post with 2 likes cuz im LAZY and this looked efficient
function toDataURL(file, callback) {
    var reader = new FileReader();
    reader.onloadend = function () {
        var dataURL = reader.result;
        callback(dataURL);
    }
    reader.readAsDataURL(file);
}