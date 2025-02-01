# 🔍 AI-Powered Research Assistant (RAG Implementation)

🚀 This project implements **Retrieval-Augmented Generation (RAG)** to create an **AI research assistant** that can:
✅ Retrieve **relevant research papers** from **arXiv**  
✅ Use **Qdrant (Vector Database)** for **efficient similarity search**  
✅ Leverage **DeepSeek R1 (via Ollama)** to **generate AI-powered answers**  
✅ Allow **uploading research papers (PDFs)** for **AI-driven critiques**  
✅ Stream responses in **real-time** via **FastAPI**

---

## 📌 **Tech Stack**
- **LLM**: DeepSeek R1 (via Ollama)
- **Retrieval**: Qdrant (Vector Database)
- **Embeddings**: Sentence-Transformers (`all-MiniLM-L6-v2`)
- **Web API**: FastAPI
- **Data Source**: arXiv API
- **Orchestration**: LangChain

---

## 🚀 **Features**
✅ **RAG-based AI responses** → Retrieves papers before generating answers  
✅ **Real-time streaming** → AI generates responses dynamically  
✅ **Citation-aware generation** → Provides sources from real research papers  
✅ **Multi-turn conversations** → AI remembers past queries  
✅ **Research Paper Upload** → AI critiques uploaded **PDFs**  

---

## 🔧 **Setup & Installation**
### **1️⃣ Clone the repository**
```sh
git clone https://github.com/YOUR_GITHUB_USERNAME/rag-research-assistant.git
cd rag-research-assistant
