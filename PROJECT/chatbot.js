const chatBox = document.getElementById('chatBox');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');

// Helper function to create message bubbles
// Helper function to create message bubbles
function appendMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    
    if (sender === 'user') {
        messageDiv.classList.add('user-message');
        // Keep user text as plain text
        messageDiv.textContent = text; 
    } else {
        messageDiv.classList.add('bot-message');
        // Translate the bot's Markdown into HTML
        messageDiv.innerHTML = marked.parse(text); 
    }

    chatBox.appendChild(messageDiv);
    
    // Auto-scroll to the newest message
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Main logic for sending a message
async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    // 1. Display the user's message
    appendMessage(text, 'user');
    userInput.value = ''; // Clear input

    // 2. Show a temporary loading message
    appendMessage("Analyzing athlete data...", 'bot');
    const typingMessage = chatBox.lastChild; 

    // 3. HTTP Request to Python Server (Placeholder for Step 2)
    try {
        const response = await fetch('http://127.0.0.1:5000/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });
        const data = await response.json();
        
        // Remove typing indicator and show real RAG response
        chatBox.removeChild(typingMessage);
        appendMessage(data.reply, 'bot');
    } catch (error) {
        chatBox.removeChild(typingMessage);
        appendMessage("Error: Could not connect to the backend server.", 'bot');
    }
}

// Trigger send on button click or 'Enter' key press
sendBtn.addEventListener('click', sendMessage);

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});