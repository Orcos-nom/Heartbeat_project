async function sendMessage() {

    const input = document.getElementById("chat-input")
    const body = document.getElementById("chat-body")

    const msg = input.value

    body.innerHTML += `<div><b>You:</b> ${msg}</div>`

    input.value = ""

    const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: msg })
    })

    const data = await res.json()

    body.innerHTML += `<div><b>AI:</b> ${data.reply}</div>`

    body.scrollTop = body.scrollHeight
}