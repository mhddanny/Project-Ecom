// Variable
    let chatName = ''
    let chatSocket = null
    let chatWindowUrl = window.location.href
    let chatRoomUuid = Math.random().toString(36).slice(2, 12)

    //Elements
    const chatWelcomeElement = document.getElementById("chat_welcome");
    const chatRoomElement = document.getElementById("chat_room");
    
    const chatCheckElement = document.querySelector('#check');
    const chatJoinElement = document.querySelector('#chat_join');
    const chatNameElement = document.querySelector('#chat_name');
    const chatInputElement = document.querySelector('#chat_message_input');
    const chatSubmitElement = document.querySelector('#chat_message_submit');

    // Function
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
        chatSocket.send(JSON.stringify({
            'type': 'message',
            'message': chatInputElement.value,
            'name': chatName
        }))

        chatInputElement.value = ''
    }

    async function joinChatRomm(){
        // console.log('joinChatRoom')
        chatName = chatNameElement.value

        console.log('join as :', chatName)
        console.log('Room id :', chatRoomUuid)

        const data = new FormData()
        data.append('name', chatName)
        data.append('url', chatWindowUrl)

        await fetch(`/chat/api/create-room/${chatRoomUuid}/`, {
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

        const chatSocket = new WebSocket(`ws://${window.location.host}/ws/${chatRoomUuid}/`);

        chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            console.log(onmessage)
        }

        chatSocket.onopen = function(e) {
            console.log('onopen - chat socket was opened')
        }

        chatSocket.onclose = function(e) {
            console.log('onClose - chat socket was closed')
        }

    }


    //listeners
    
    chatCheckElement.onclick = function(e) {
        chatWelcomeElement.classList.remove("hidden");
    }

    chatJoinElement.onclick = function(e) {
        chatRoomElement.classList.remove("hidden");
        chatWelcomeElement.classList.add("hidden");

        
        console.log('test')

        joinChatRomm();

    }

    chatSubmitElement.onclick = function(e) {
        // e.preventDefault()
        
        // sendMessage()

        chatSocket.send(JSON.stringify({
            'type': 'message',
            'message': chatInputElement.value,
            'name': chatName
        }))

        chatInputElement.value = ''
    }
