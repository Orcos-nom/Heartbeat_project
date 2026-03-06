function toggleChat() {

    const box = document.getElementById("chatbox");

    box.style.display = box.style.display === "none" ? "block" : "none";

}

async function sendMessage() {

    const input = document.getElementById("input").value;

    const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {

        method: "POST",

        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer YOUR_OPENROUTER_API_KEY"
        },

        body: JSON.stringify({

            model: "openai/gpt-3.5-turbo",

            messages: [
                { role: "user", content: input }
            ]

        })

    });

    const data = await response.json();

    document.getElementById("messages").innerHTML += "<div>" + data.choices[0].message.content + "</div>";

}