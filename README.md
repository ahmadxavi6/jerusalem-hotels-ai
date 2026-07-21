# 🏨 Jerusalem Hotels AI Concierge

A production-grade AI-powered hotel recommendation chatbot for Jerusalem tourists, built with RAG (Retrieval Augmented Generation) using Claude API and Supabase pgvector.

🌐 **Live Demo:** https://jerusalem-hotels-ai-production.up.railway.app/

---

## ✨ Features

- 🤖 **RAG System** — semantic vector search using pgvector, answers based on real hotel database not AI training data
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
```

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python + Flask |
| AI | Claude API (Anthropic) — streaming |
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
├── claude_client.py        # Claude API + streaming responses
├── admin.py                # Admin panel blueprint + CRUD
├── seed.py                 # One-time database seeding with embeddings
├── static/
│   ├── css/main.css        # Ocean Blue responsive UI
│   └── js/chat.js          # Streaming frontend + compare logic
├── templates/
│   ├── index.html          # Chat UI
│   └── admin/              # Admin panel templates
│       ├── login.html
│       ├── dashboard.html
│       ├── add.html
│       └── edit.html
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