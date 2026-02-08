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
        + '/ws/monopoly/'
        + roomName
        + '/'
} else {
    connection = 'ws://'
        + window.location.host
        + '/ws/monopoly/'
        + roomName
        + '/'
}

const chatSocket = new WebSocket(connection)


// Since chromebooks disable inspection, since is a fake console. display references that text.
const display = document.getElementById("console");

// grid references the monopoly board
const grid = document.getElementsByClassName("board")[0];

console.log("hello");

for (let i = 0; i < 36; i++) {
    // Adds tiles to monopoly, except for the already defined corners.

    // Item is the tile
    let item = document.createElement("div");
    // Span is the text that has the id
    let span = document.createElement("span");

    // Sets the text in the tile to its id, but since corners are not accounted for, its not completely accurate.

    span.classList.add("span");
    item.classList.add("item");


    if (i >= 9 && i <= 26) {
        if (i % 2 === 0) {
            // Rotates tiles on the right side, so the text faces the correct way
            span.classList.add("right")
            item.id = String(32 + (i - 10) / 2);
        } else {
            // Rotates tiles on the left  side, so the text faces the correct way
            span.classList.add("left");
            item.id = String(24 - (i - 1) / 2);

        }
    }
    // Sets the id, so javascript can reference it easily
    if (i <= 8) {
        item.id = String(22 + i);
    } else if (i > 26) {
        item.id = String(10 - (i - 27));
    }

    span.textContent = item.id;
    // Adds the text to the tiles
    item.append(span);
    // Adds the tile to the grid
    grid.append(item);
}

// Creates an image that is the player
const player = document.createElement('img');
// Makes the image a hat
player.src = "/static/monopoly/monopoly_piece_1.svg";
// Lets javascript know what the player is referenced as
player.id = "monopoly-1";
// Gives the player a class, so the CSS makes it pretty
player.className = "piece";

// Starts by putting the player in tile 2
document.getElementById("2").appendChild(player);

chatSocket.onopen = function (event) {
    const data = event.data;
    console.log(data.message);
    display.innerHTML = data.message + " Press R to roll.";
}