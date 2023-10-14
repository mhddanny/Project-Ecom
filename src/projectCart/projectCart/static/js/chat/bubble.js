/**
 * Element
 */
let chatName = ''
let chatSocket = null
let chatWindowUrl = window.location.href
let chatRoomUuid = Math.random().toString(36).slice(2, 12)

//Elements
const chatWelcomeElement = document.getElementById("chat_welcome");
const chatRoomElement = document.getElementById("chat_room");

const chatCheckElement = document.querySelector('#check');
const chatJoinElement = document.querySelector('#chat_join');
const chatLogElement = document.querySelector('#chat_log');
const chatNameElement = document.querySelector('#chat_name');
const chatInputElement = document.querySelector('#chat_message_input');
const chatSubmitElement = document.querySelector('#chat_message_submit');

/**
 * Function
 *  */ 

function scrollToBottom() {
    chatLogElement.scrollTop = chatLogElement.scrollHeight
}

function getCookie(name) {
    var cookieValue = null

    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';')

        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim()
            
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1))

                break
            }
        }
    }

    return cookieValue
}

function sendMessage() {
    chatSocket.send(JSON.stringify(
        {
            'type': 'message',
            'message': chatInputElement.value,
            'name': chatName
        }
    ))

    chatInputElement.value = ''
}

function onChatMessage(data) {
    console.log('onChatMessage', data)

    if (data.type == 'chat_message') {
        if (data.agent) {
            chatLogElement.innerHTML += `
                <div class="d-flex flex-row justify-content-start mb-4">
                    <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava3-bg.webp"
                        alt="avatar 1" style="width: 45px; height: 100%;" class="mr-2">
                    <div>
                        <p class="small p-2 ms-3 mb-1 rounded-3" style="background-color: #ffffff;">${data.message}</p>
                        <p class="small ms-3 mb-3 rounded-3 text-muted">${data.created_at} ago</p>
                    </div>
                </div>
            `
            
        } else {
            chatLogElement.innerHTML += `
                <div class="d-flex flex-row justify-content-end mb-4">
                    <div>
                        <p class="small p-2 me-3 mb-1 text-white rounded-3" style="background-color: #349afa;">${data.message}</p>
                        <p class="small me-3 mb-3 rounded-3 text-muted d-flex justify-content-end">${data.created_at} ago</p>
                    </div>
                    <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava4-bg.webp"
                        alt="avatar 1" style="width: 45px; height: 100%;" class="ml-2"">
                </div>
            `
        
        }
    }
    scrollToBottom()
}

async function joinChatRomm(){
    // console.log('joinChatRoom')
    chatName = chatNameElement.value

    console.log('join as :', chatName)
    console.log('Room id :', chatRoomUuid)

    const data = new FormData()
    data.append('name', chatName)
    data.append('url', chatWindowUrl)

    await fetch(`/api/create-room/${chatRoomUuid}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: data
    })
    .then(function(res) {
        return res.json()
    })
    .then(function(data) {
        console.log('data', data)
    })

    chatSocket = new WebSocket(`ws://${window.location.host}/ws/${chatRoomUuid}/`);

    chatSocket.onmessage = function(e) {
        console.log('onmessage')

        onChatMessage(JSON.parse(e.data))
    }

    chatSocket.onopen = function(e) {
        console.log('onopen - chat socket was opened')
        scrollToBottom()
    }

    chatSocket.onclose = function(e) {
        console.log('onClose - chat socket was closed')
    }

}


// listeners

chatCheckElement.onclick = function(e) {
    chatWelcomeElement.classList.remove("hidden");
}

chatJoinElement.onclick = function(e) {
    chatRoomElement.classList.remove("hidden");
    chatWelcomeElement.classList.add("hidden");

    
    console.log('test')

    joinChatRomm();

}

chatInputElement.focus()
chatInputElement.onkeyup = function(e) {
    if (e.key === 'Enter' ) {
        sendMessage()
    }
}

chatSubmitElement.onclick = function(e) {
    // e.preventDefault()
    
    sendMessage()
}

