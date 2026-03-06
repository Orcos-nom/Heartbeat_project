let recorder
let audioChunks = []
let audioBlob = null

const startBtn = document.getElementById("startBtn")
const stopBtn = document.getElementById("stopBtn")
const sendBtn = document.getElementById("sendBtn")
const loader = document.getElementById("loader")

navigator.mediaDevices.getUserMedia({ audio: true })

    .then(stream => {

        recorder = new MediaRecorder(stream)

        recorder.ondataavailable = e => {
            audioChunks.push(e.data)
        }

        recorder.onstop = () => {

            audioBlob = new Blob(audioChunks, { type: "audio/wav" })

            sendBtn.disabled = false

        }

    })


startBtn.onclick = () => {

    audioChunks = []

    recorder.start()

    startBtn.disabled = true
    stopBtn.disabled = false

}


stopBtn.onclick = () => {

    recorder.stop()

    stopBtn.disabled = true

}


sendBtn.onclick = () => {

    loader.classList.remove("hidden")

    let formData = new FormData()

    formData.append("audio", audioBlob, "heartbeat.wav")

    fetch("/upload_heartbeat", {

        method: "POST",
        body: formData

    })

        .then(res => res.json())

        .then(data => {

            localStorage.setItem("result", JSON.stringify(data))

            window.location = "/result"

        })

}