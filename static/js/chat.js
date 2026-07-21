const sessionId = Math.random().toString(36).substring(7);

function disableAll() {
    document.getElementById("input").disabled = true;
    document.querySelector(".send-btn").disabled = true;
    document.querySelector(".compare-btn").disabled = true;
    document.querySelector(".agent-btn").disabled = true;
}

function enableAll() {
    document.getElementById("input").disabled = false;
    document.querySelector(".send-btn").disabled = false;
    document.querySelector(".compare-btn").disabled = false;
    document.querySelector(".agent-btn").disabled = false;
    document.getElementById("input").focus();
}

async function streamResponse(url, body, botSpan, chat) {
    let fullText = "";
    let typingQueue = Promise.resolve();

    async function typeChunk(chunk) {
        for (const char of chunk) {
            fullText += char;
            botSpan.innerHTML = marked.parse(fullText);
            chat.scrollTop = chat.scrollHeight;
            await new Promise((r) => setTimeout(r, 15));
        }
    }

    const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value);
        const lines = chunk.split("\n");
        for (const line of lines) {
            if (line.startsWith("data: ")) {
                const raw = line.slice(6);
                if (raw === "[DONE]") continue;
                try {
                    const text = JSON.parse(raw);
                    typingQueue = typingQueue.then(() => typeChunk(text));
                } catch (e) {}
            }
        }
    }

    await typingQueue;
    botSpan.innerHTML = marked.parse(fullText);
    chat.scrollTop = chat.scrollHeight;
}

function createBotMessage(chat, initialText = "...") {
    const botDiv = document.createElement("div");
    botDiv.className = "message bot-msg";
    const botSpan = document.createElement("span");
    botSpan.innerHTML = initialText;
    botDiv.appendChild(botSpan);
    chat.appendChild(botDiv);
    chat.scrollTop = chat.scrollHeight;
    return botSpan;
}

async function sendMessage() {
    const input = document.getElementById("input");
    const chat = document.getElementById("chat");
    const question = input.value.trim();
    if (!question) return;

    disableAll();
    addMessage(question, "user");
    input.value = "";

    const botSpan = createBotMessage(chat);
    await streamResponse("/ask-stream", { question, session_id: sessionId }, botSpan, chat);
    enableAll();
}

async function sendAgent() {
    const input = document.getElementById("input");
    const chat = document.getElementById("chat");
    let question = input.value.trim();
    if (!question) {
        question = "Based on our conversation so far, find me the perfect hotel.";
    }

    disableAll();
    addMessage(question, "user");
    input.value = "";

    const botSpan = createBotMessage(chat, "🎯 Finding your perfect hotel...");
    await streamResponse("/agent", { question, session_id: sessionId }, botSpan, chat);
    enableAll();
}

async function compareHotels() {
    const hotel1 = document.getElementById("hotel1").value.trim();
    const hotel2 = document.getElementById("hotel2").value.trim();
    const chat = document.getElementById("chat");

    if (!hotel1 || !hotel2) {
        alert("Please enter both hotel names");
        return;
    }

    disableAll();
    addMessage(`Compare ${hotel1} vs ${hotel2}`, "user");

    const botSpan = createBotMessage(chat, "🔄 Comparing hotels...");
    await streamResponse("/compare-stream", { hotel1, hotel2, session_id: sessionId }, botSpan, chat);

    document.getElementById("hotel1").value = "";
    document.getElementById("hotel2").value = "";
    enableAll();
}

async function quickAsk(question) {
    const input = document.getElementById("input");
    if (input.disabled) return;
    input.value = question;
    await sendMessage();
}

function addMessage(text, type) {
    const chat = document.getElementById("chat");
    const div = document.createElement("div");
    div.className = `message ${type}-msg`;
    const span = document.createElement("span");
    if (type === "bot") {
        span.innerHTML = marked.parse(text);
    } else {
        span.textContent = text;
    }
    div.appendChild(span);
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

function toggleSidebar() {
    const sidebar = document.querySelector(".sidebar");
    const overlay = document.querySelector(".sidebar-overlay");
    sidebar.classList.toggle("open");
    overlay.classList.toggle("open");
}