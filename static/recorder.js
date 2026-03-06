let mediaRecorder;
let chunks = [];

document.getElementById("start").onclick = async () => {

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.start();

    mediaRecorder.ondataavailable = e => {
        chunks.push(e.data);
    };

};

document.getElementById("stop").onclick = () => {

    mediaRecorder.stop();

    mediaRecorder.onstop = async () => {

        const blob = new Blob(chunks, { type: "audio/wav" });

        chunks = [];

        document.getElementById("audio").src = URL.createObjectURL(blob);

        const formData = new FormData();

        formData.append("file", blob, "recording.wav");
        formData.append("type", uploadType);

        await fetch("/upload", {
            method: "POST",
            body: formData
        });

        alert("Audio uploaded to GitHub");

    };

};