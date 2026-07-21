const sessionId = Math.random().toString(36).substring(7);

async function sendMessage() {
  const input = document.getElementById("input");
  const chat = document.getElementById("chat");
  const question = input.value.trim();
  if (!question) return;

  // Disable input while streaming
  input.disabled = true;
  input.disabled = true;
  document.querySelector(".send-btn").disabled = true;
  document.querySelector(".compare-btn").disabled = true;

  addMessage(question, "user");
  input.value = "";

  const botDiv = document.createElement("div");
  botDiv.className = "message bot-msg";
  const botSpan = document.createElement("span");
  botSpan.innerHTML = "...";
  botDiv.appendChild(botSpan);
  chat.appendChild(botDiv);
  chat.scrollTop = chat.scrollHeight;

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

  const response = await fetch("/ask-stream", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, session_id: sessionId }),
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

  // Re-enable at the end
  input.disabled = false;
  document.querySelector(".send-btn").disabled = false;
  document.querySelector(".compare-btn").disabled = false;

  input.focus();
}
async function quickAsk(question) {
  document.getElementById("input").value = question;
  await sendMessage();
}

async function compareHotels() {
    const hotel1 = document.getElementById('hotel1').value.trim();
    const hotel2 = document.getElementById('hotel2').value.trim();
    const chat = document.getElementById('chat');

    if (!hotel1 || !hotel2) {
        alert('Please enter both hotel names');
        return;
    }

    // Disable everything
    document.querySelector('.compare-btn').disabled = true;
    document.querySelector('.send-btn').disabled = true;
    document.getElementById('input').disabled = true;

    addMessage(`Compare ${hotel1} vs ${hotel2}`, 'user');

    const botDiv = document.createElement('div');
    botDiv.className = 'message bot-msg';
    const botSpan = document.createElement('span');
    botSpan.innerHTML = '...';
    botDiv.appendChild(botSpan);
    chat.appendChild(botDiv);
    chat.scrollTop = chat.scrollHeight;

    let fullText = '';
    let typingQueue = Promise.resolve();

    async function typeChunk(chunk) {
        for (const char of chunk) {
            fullText += char;
            botSpan.innerHTML = marked.parse(fullText);
            chat.scrollTop = chat.scrollHeight;
            await new Promise(r => setTimeout(r, 15));
        }
    }

    const response = await fetch('/compare-stream', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({hotel1, hotel2, session_id: sessionId})
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
        const {done, value} = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');
        for (const line of lines) {
            if (line.startsWith('data: ')) {
                const raw = line.slice(6);
                if (raw === '[DONE]') continue;
                try {
                    const text = JSON.parse(raw);
                    typingQueue = typingQueue.then(() => typeChunk(text));
                } catch(e) {}
            }
        }
    }

    await typingQueue;
    botSpan.innerHTML = marked.parse(fullText);
    chat.scrollTop = chat.scrollHeight;

    document.querySelector('.compare-btn').disabled = false;
    document.querySelector('.send-btn').disabled = false;
    document.getElementById('input').disabled = false;
    document.getElementById('hotel1').value = '';
    document.getElementById('hotel2').value = '';
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

async function quickAsk(question) {
  const input = document.getElementById("input");
  if (input.disabled) return; // prevent if already typing
  input.value = question;
  await sendMessage();
}
