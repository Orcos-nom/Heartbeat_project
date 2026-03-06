function toggleChat() {

    let box = document.getElementById("assistant")

    box.style.display = box.style.display === "flex" ? "none" : "flex"

}



async function sendMessage() {

    let input = document.getElementById("chat-input-box")

    let msg = input.value

    let chat = document.getElementById("chat-messages")

    chat.innerHTML += `<p><b>You:</b> ${msg}</p>`

    let r = await fetch("/chatbot", {

        method: "POST",

        headers: { "Content-Type": "application/json" },

        body: JSON.stringify({ message: msg })

    })

    let data = await r.json()

    chat.innerHTML += `<p><b>Assistant:</b> ${data.reply}</p>`

    input.value = ""

    chat.scrollTop = chat.scrollHeight

}