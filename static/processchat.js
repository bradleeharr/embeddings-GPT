var socket = io.connect('http://' + document.domain + ':' + location.port);
var receivingResponse = false;
var collectedResponse = "Bot: ";
var converter = new showdown.Converter();  // Initialize the converter once at the beginning
socket.on('response', function(msg) {
    console.log('response: ', msg)
    let chatbox = document.getElementById("chatbox");
    if (msg) collectedResponse += msg;
    if (!receivingResponse && msg) {
        console.log("CreateDiv", msg)
        chatbox.innerHTML += "<div class='message bot'> " + collectedResponse;
        receivingResponse = true;
    }
    else if (msg == ".\n\n") {
        var formattedResponse = converter.makeHtml(collectedResponse);
        chatbox.lastChild.innerHTML = formattedResponse;
    }
    else if (msg) {
        chatbox.lastChild.innerHTML += msg;
    }
    chatbox.scrollTop = chatbox.scrollHeight;
});


socket.on('stop_reason', function(msg) {
    console.log("STOP");
    let chatbox = document.getElementById("chatbox");
    var formattedResponse = converter.makeHtml(collectedResponse);
    chatbox.lastChild.innerHTML = formattedResponse + "</div>";
    collectedResponse = "Bot: ";  // reset the collected response
    receivingResponse = false;
});

function sendMessage() {
    let message = document.getElementById("userInput").value;
    socket.send(message);
    document.getElementById("userInput").value = "";

    let chatbox = document.getElementById("chatbox");
    chatbox.innerHTML += "<div class='message user'>You: " + message + "</div>";
}
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("userInput").addEventListener("keydown", function(e) {
      if(e.keyCode === 13 && e.shiftKey) {
        e.preventDefault();
        // Insert a new line at the cursor position
        this.value = this.value.substring(0, this.selectionStart) + "\n" + this.value.substring(this.selectionEnd);
        // Update the cursor position
        this.selectionStart = this.selectionEnd = this.selectionStart + 1;
    } else if (e.key === "Enter") {
        e.preventDefault();
        sendMessage();
    }
    });
});





