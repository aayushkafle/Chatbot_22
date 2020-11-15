const submitButton = document.getElementById('send-button');
const chatbotInput = document.getElementById('chatbot-input');
const chatbotOutput = document.getElementById('chatbot-output');
const chat = document.getElementsByClassName('chat')[0];

submitButton.onclick = userSubmitEventHandler;
chatbotInput.onkeyup = userSubmitEventHandler;

//This function is an event handler for submitting a message by pressing Enter (Return key on keyboard) or clicking directly on the button by mouse.
function userSubmitEventHandler(event) {
    if (
        (event.keyCode && event.keyCode === 13) ||
        event.type === 'click'
    ) {
        //chatbotOutput.innerText = 'thinking...';
        askChatBot(chatbotInput.value);
        
        //This section is used to show the message on the GUI.
        inp = document.createElement("DIV");
        inp.className = "message"
        inpCon = document.createElement("DIV");
        inpCon.className = "mine messages"
      
        //The message's text that would be indicated now gets its value here.  
        inp.innerText = chatbotInput.value;
        inpCon.appendChild(inp);
        document.getElementsByClassName('chat')[0].appendChild(inpCon);
        
        //To remove the message from the typing section after sending it.
        chatbotInput.value='';
        chat.scrollTop = chat.scrollHeight;
    }
}


//This function gets a new message from user and sends it to the server.
function askChatBot(userInput) {
    
    const myRequest = new Request('/', {
        method: 'POST',
        body: userInput
    });

    //Send request to a resource
    fetch(myRequest).then(function(response) {
       
        //This section checks the request's situation out.
        if (!response.ok) {
            throw new Error('HTTP error, status = ' + response.status);
        } else {
            return response.text();
        }
    }).then(function(text) {
        
        //This section shows the chatbot's reply in the GUI with the same procedure as we saw for indicating user messages.
        chatbotInput.value = '';
        out = document.createElement("DIV");
        out.className = "message"
        outCon = document.createElement("DIV");
        outCon.className = "yours messages"
        out.innerText = text;
        outCon.appendChild(out);
        document.getElementsByClassName('chat')[0].appendChild(outCon);
    }).catch((err) => {
        console.error(err);
    });
}
