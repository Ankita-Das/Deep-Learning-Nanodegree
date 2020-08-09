
function render_single_message(message, category){
    if (message != ""){
        var message_section = document.getElementsByClassName("messages")[0];
        var new_message = document.createElement("div");
        new_message.innerHTML = message

        message_section.appendChild(new_message);

        if (category=="bot"){
            new_message.className = "message-bot";
        }

        if (category=="user"){
            new_message.className = "message-user";
        }
    }
}

function render_bot_message(message){
    render_single_message(message, "bot");
}

function render_user_message(message){
    render_single_message(message, "user");
}

function send_request(){
    var message = document.getElementsByClassName("message-text-field")[0];
    var http = new XMLHttpRequest();
    var url = document.getElementById("post-url").getAttribute("url");

    http.open("POST", url, true);
    http.setRequestHeader("Content-Type", "application/json");

    var data = JSON.stringify({'user_message':message.value});

    render_user_message(message.value);
    http.send(data);
    message.value = "";

    http.onreadystatechange = function () {
        if (http.readyState === 4 && http.status === 200) {
            var response = http.responseText;
            render_bot_message(response);
        }
    };
}

button = document.getElementsByClassName("send-button")[0];
button.addEventListener("click", send_request);
