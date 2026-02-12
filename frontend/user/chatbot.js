const icon = document.getElementById("chatbot-icon");
const box = document.getElementById("chatbot-box");
const closeBtn = document.getElementById("close-chat");
const sendBtn = document.getElementById("send-btn");
const input = document.getElementById("user-input");
const messages = document.getElementById("chatbot-messages");

// Backend URL
const API_URL = "http://127.0.0.1:8000/chat";

// Chat state
let chatbotOpen = false;
let isSending = false; // 🔒 prevents double submit (CRITICAL)

// Open chatbot
icon.onclick = () => {
  box.style.display = "flex";
  chatbotOpen = true;

  if (messages.children.length === 0) {
    addMessage(
      "Hi 👋 I’m the Sciqus AMS assistant. ",
      "bot"
    );
  }
};

// Close chatbot
closeBtn.onclick = () => {
  box.style.display = "none";
  chatbotOpen = false;
};

// Send on button click
sendBtn.onclick = () => {
  sendMessage();
};

// Send on Enter key
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    e.preventDefault(); // 🔥 REQUIRED
    sendMessage();
  }
});

function addMessage(text, sender) {
  if (!chatbotOpen) return;

  const div = document.createElement("div");
  div.className = `message ${sender}`;

  if (sender === "bot") {
    // Make links clickable
    div.innerHTML = text.replace(
      /(https?:\/\/[^\s]+)/g,
      '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'
    );
  } else {
    div.innerText = text;
  }

  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}

async function sendMessage() {
  // 🔒 BLOCK DOUBLE CALLS
  if (isSending) return;
  isSending = true;

  const question = input.value.trim();
  if (!question) {
    isSending = false;
    return;
  }

  addMessage(question, "user");
  input.value = "";

  // Typing indicator
  const typing = document.createElement("div");
  typing.className = "message bot";
  typing.innerText = "Sciqus AI is thinking…";
  messages.appendChild(typing);
  messages.scrollTop = messages.scrollHeight;

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ question })
    });

    if (!res.ok) {
      throw new Error("Backend error");
    }

    const data = await res.json();

    typing.remove();
    addMessage(
      data.answer ||
        "Thanks! Our team will review this and reach out if needed.",
      "bot"
    );

  } catch (err) {
    console.error("Chatbot error:", err);
    typing.remove();
    addMessage(
      "The assistant is temporarily unavailable. Please try again later.",
      "bot"
    );
  } finally {
    isSending = false; // 🔓 unlock
  }
}

// Prevent mobile Enter from submitting twice
document.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
  }
});
