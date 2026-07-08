window.onload = () => {
    loadTheme();
};

//  THEME
function loadTheme() {
    let savedTheme = localStorage.getItem("theme");

    if (savedTheme === "dark") {
        document.body.classList.add("dark");
        document.querySelector(".toggle").innerText = "☀ Light";
    } else {
        document.querySelector(".toggle").innerText = "🌙 Dark";
    }
}

function toggleTheme() {
    document.body.classList.toggle("dark");

    let isDark = document.body.classList.contains("dark");

    localStorage.setItem("theme", isDark ? "dark" : "light");

    document.querySelector(".toggle").innerText =
        isDark ? "☀ Light" : "🌙 Dark";
}


//  ASK AI
async function sendMessage() {
    let input = document.getElementById("question").value;

    if (!input) return;

    document.getElementById("answer").innerText = "Thinking... 🤖";

    let response = await fetch("/ask", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ question: input })
    });

    let data = await response.json();

    document.getElementById("answer").innerText = data.answer;
}


//  OCR
async function uploadImage() {
    let fileInput = document.getElementById("imageInput");
    let file = fileInput.files[0];

    if (!file) {
        alert("Select an image first 📷");
        return;
    }

    let formData = new FormData();
    formData.append("image", file);

    document.getElementById("ocrResult").innerText = "Scanning... 📷";

    let response = await fetch("/upload", {
        method: "POST",
        body: formData
    });

    let data = await response.json();

    document.getElementById("ocrResult").innerText = data.text;
}


//  MCQ
async function generateMCQ() {
    document.getElementById("mcq").innerText = "Generating... 🧠";

    let response = await fetch("/generate_mcq");
    let data = await response.json();

    document.getElementById("mcq").innerText = data.mcq;
}

function clearOutputs() {
    document.getElementById("ocrResult").innerText = "";
    document.getElementById("answer").innerText = "";
    document.getElementById("mcq").innerText = "";
}