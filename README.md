# 🏨 Jerusalem Hotels AI Concierge

A production-grade AI-powered hotel recommendation chatbot for Jerusalem tourists, built with RAG (Retrieval Augmented Generation) and an AI Agent using Claude API and Supabase pgvector.


---


## 🎯 About This Project

This project is not about hotels — it's about demonstrating production-grade AI engineering patterns:

- **RAG over fine-tuning** — instead of retraining a model, we inject private data at query time using vector similarity search
- **AI Agents with Tool Use** — Claude autonomously decides which tools to call and in what order, reasoning through competing user preferences
- **Semantic search over keyword search** — pgvector finds "budget accommodation near holy sites" even if those exact words don't appear in the database
- **Streaming over batch** — responses stream token by token like ChatGPT, reducing perceived latency
- **Prompt engineering for safety** — the system refuses off-topic queries and prevents hallucination by grounding Claude strictly in retrieved context


## ✨ Features

- 🤖 **RAG System** — semantic vector search using pgvector, answers based on real hotel database not AI training data
- 🎯 **AI Agent** — Claude autonomously uses tools to find your perfect hotel based on vibe, budget and preferences
- ⚡ **Streaming Responses** — ChatGPT-style real-time typing effect
- 💬 **Conversation Memory** — remembers budget and preferences throughout the chat
- 💰 **Smart Budget Filter** — automatically filters hotels within your budget
- 💱 **Live Currency Conversion** — real-time USD, EUR, GBP, NIS exchange rates
- 🔄 **Hotel Comparison** — streaming side-by-side comparison tables
- 🌍 **Multi-language** — English, Arabic, Hebrew
- 🔒 **Security** — topic restricted via prompt engineering, hallucination prevention
- 📱 **Mobile Responsive** — sidebar drawer navigation on mobile
- 🛠️ **Admin Panel** — full CRUD interface to manage hotels at `/admin`
- 🐳 **Docker** — containerized for easy local deployment

## 🎯 AI Agent — How It Works

The 🎯 Match button triggers an AI agent that:

1. Reads your **entire conversation history** to extract preferences
2. Autonomously decides which **tools to call** (search_hotels, get_all_hotels)
3. **Reasons through tradeoffs** — e.g. pool vs proximity to Al-Aqsa
4. Picks the **single best hotel** with a clear explanation
5. References **specific things you mentioned** earlier in the conversation

This is Claude's **Tool Use API** in action — not a simple chatbot but an autonomous agent making decisions.

**Example:**
```
User: "I like pools"
User: "budget around $100"
User: "I want to be close to Al-Aqsa"
→ Click 🎯 Match
→ Agent searches database with all 3 preferences
→ Finds conflict: pool hotels are far from Al-Aqsa
→ Makes judgment call: location > pool
→ Picks Hashimi Hotel and explains the tradeoff
```

## 🏗️ Architecture

```
User Question
      ↓
sentence-transformers (convert question to 384-dim vector)
      ↓
Supabase pgvector (cosine similarity search)
      ↓
Budget filter + Currency detection
      ↓
Claude API with streaming (answer based on relevant hotels + history)
      ↓
User gets streamed answer in their language and currency

🎯 Agent Mode:
User preferences (from full conversation history)
      ↓
Claude Agent (Tool Use API)
      ↓
Autonomous tool calls → search_hotels, get_all_hotels
      ↓
Reasoning through tradeoffs
      ↓
Single best recommendation with explanation
```

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python + Flask |
| AI | Claude API (Anthropic) — streaming + tool use |
| Vector DB | Supabase + pgvector |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Frontend | HTML + CSS + JavaScript |
| Admin | Flask Blueprint + session auth |
| Deployment | Railway |
| Container | Docker |

## 🚀 Setup

**1. Clone the repo**
```bash
git clone https://github.com/ahmadxavi6/jerusalem-hotels-ai.git
cd jerusalem-hotels-ai
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Create `.env` file**
```
ANTHROPIC_API_KEY=your-claude-api-key
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_KEY=your-supabase-anon-key
ADMIN_PASSWORD=your-admin-password
SECRET_KEY=any-random-string
```

**4. Seed the database (run once)**
```bash
python seed.py
```

**5. Run**
```bash
python app.py
```

**6. Open** http://localhost:5000

## 🐳 Docker

```bash
docker build -t jerusalem-hotels .
docker run -p 5000:5000 --env-file .env jerusalem-hotels
```

## 🛠️ Admin Panel

Access at `/admin` with your admin password.

- View all hotels in a dashboard table
- Add new hotels — embedding generated automatically
- Edit existing hotels — embedding regenerated automatically
- Delete hotels

## 📁 Project Structure

```
jerusalem-hotels-ai/
├── app.py                  # Flask routes + streaming endpoints
├── rag.py                  # Supabase pgvector search + budget/currency filter
├── claude_client.py        # Claude API + streaming + agent tool use
├── admin.py                # Admin panel blueprint + CRUD
├── seed.py                 # One-time database seeding with embeddings
├── static/
│   ├── css/main.css        # Ocean Blue responsive UI
│   └── js/chat.js          # Streaming frontend + agent + compare logic
├── templates/
│   ├── index.html          # Chat UI
│   └── admin/              # Admin panel templates
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .gitignore
```

## 💡 How RAG Works

1. Hotel data stored in Supabase PostgreSQL with pgvector extension
2. Each hotel converted to a 384-dimension vector using sentence-transformers
3. User question converted to same vector space
4. pgvector finds most semantically similar hotels using cosine similarity
5. Budget filter applied based on detected currency and amount
6. Relevant hotels + full conversation history sent to Claude API
7. Claude streams answer based on YOUR data — not its training data

## 🔒 Security

- API keys in `.env` — never uploaded to GitHub
- Admin panel protected by session-based password authentication
- Chatbot restricted to hotel topics via prompt engineering
- Users cannot override system instructions
- Hallucination prevention — Claude only answers from provided context
