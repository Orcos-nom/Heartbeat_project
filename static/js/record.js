let recorder
let chunks = []

const recordBtn = document.getElementById("recordBtn")
const processing = document.getElementById("processing")

navigator.mediaDevices.getUserMedia({ audio: true })

    .then(stream => {

        recorder = new MediaRecorder(stream)

        recorder.ondataavailable = e => chunks.push(e.data)

        recorder.onstop = () => {

            let blob = new Blob(chunks, { type: "audio/wav" })

            let file = new File([blob], "heartbeat.wav")

            processing.classList.remove("hidden")

            let form = new FormData()

            form.append("audio", file)

            fetch("/upload_heartbeat", {

                method: "POST",

                body: form

            })

                .then(res => res.json())

                .then(data => {

                    localStorage.setItem("result", JSON.stringify(data))

                    window.location = "/result"

                })

        }

    })


recordBtn.onclick = () => {

    chunks = []

    recorder.start()

    recordBtn.innerHTML = "Recording..."

    setTimeout(() => {

        recorder.stop()

    }, 5000)

}