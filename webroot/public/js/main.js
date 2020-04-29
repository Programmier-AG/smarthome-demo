 /*
    Smart-Home (Modell) - Erlebnistag 14. September 2019
    
    Dieses Script ist zur Datenübertragung zum Webserver.

    Copyright (c) 2019 Fabian Reinders, Sönke Klock
*/

 console.log("=======================================================");
 console.log("  Smart-Home (Modell) - Erlebnistag 14. September 2019 ");
 console.log(" Dieses Script ist zur Datenübertragung zum Webserver. ");
 console.log("    Copyright (c) 2019 Fabian Reinders, Sönke Klock    ");
 console.log("=======================================================");
 var ws;

function init() {
    ws = new WebSocket("ws://localhost:2687/");

    ws.onmessage = function (e) {
        console.log("RECEIVED >> " + e.data);
        toggler = document.getElementById(e.data.replace("off", "on"));

        if (toggler) {
            action = e.data.includes("on");
            toggler.checked = action;
        }
    };

    ws.onerror = function (e) {
        console.log(e);
    };
 }

function onSubmit(name, value) {
    ws.send(`${name},,,${value}`);
}

function onCloseClick() {
    ws.close();
}

function tts() {
    let ttsMessage = document.getElementById("tts-input-field").value;
    onSubmit("tts", ttsMessage);
}

allTogglers = document.querySelectorAll("input.toggler");
togglersArray = [].slice.call(allTogglers);

togglersArray.forEach(toggler => {
    toggler.addEventListener("change", togglerElement => {
        if (togglerElement.target.checked) {
            messageToServerArray = togglerElement.target.id.split("//");
            messageToServerArray[2] = "on";
            console.log("SENDING >> ('" + messageToServerArray[0] + "', '" + messageToServerArray.slice(1) + "')");
            onSubmit(messageToServerArray[0], messageToServerArray[1] + "//" + messageToServerArray[2] + "//" + messageToServerArray[3]);
        } else {
            messageToServerArray = togglerElement.target.id.split("//");
            messageToServerArray[2] = "off";
            console.log("SENDING >> ('" + messageToServerArray[0] + "', '" + messageToServerArray.slice(1) + "')");
            onSubmit(messageToServerArray[0], messageToServerArray[1] + "//" + messageToServerArray[2] + "//" + messageToServerArray[3]);
        }
    });
});