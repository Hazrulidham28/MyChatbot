function initializeChatbot() {
    const chatBox = document.getElementById("chat-box");
    const greeting = `<div class="message bot-message">Hello! I'm here to help you. Ask me anything!</div>`;
    chatBox.innerHTML += greeting;
}

async function handleUserInput(message) {
    const chatBox = document.getElementById("chat-box");

    // Display user message
    chatBox.innerHTML += `<div class="message user-message"><a>${message}</a></div>`;

    // Add typing indicator
    const typingIndicator = `<div id="typing-indicator" class="message bot-message">Typing...</div>`;
    chatBox.innerHTML += typingIndicator;
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        // Fetch bot response
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: new URLSearchParams({ query: message }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Replace typing indicator with bot response
        document.getElementById("typing-indicator").remove();
        chatBox.innerHTML += `<div class="message bot-message">${data.response}</div>`;
    } catch (error) {
        document.getElementById("typing-indicator").remove();
        chatBox.innerHTML += `<div class="message bot-message error">Oops! Something went wrong. Please try again later.</div>`;
        console.error("Error fetching bot response:", error);
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}

document.addEventListener("DOMContentLoaded", () => {
    initializeChatbot();

    document.getElementById("chat-form").onsubmit = function (e) {
        e.preventDefault();
        const input = document.getElementById("chat-input");
        const message = input.value.trim();
        if (!message) return;

        input.value = "";
        handleUserInput(message);
    };
});
