# 📚 AI Study Partner - Your Personal Learning Companion

An intelligent chatbot that transforms your syllabus PDFs into an interactive study assistant. Ask questions, get instant answers, and study smarter with AI-powered retrieval-augmented generation (RAG).

## 🌟 Features

- **📄 Multi-PDF Support** - Upload multiple syllabus files, textbooks, and study materials
- **🤖 AI-Powered Answers** - Get accurate responses based on your documents using Groq's fast LLM
- **💬 Conversational Interface** - Natural chat experience with conversation memory
- **🔍 Source Citations** - View exact passages used to generate answers for verification
- **⚡ Fast Vector Search** - FAISS-powered semantic search for quick information retrieval
- **🎯 Context-Aware** - Maintains conversation history for follow-up questions
- **🎨 User-Friendly UI** - Clean, intuitive Streamlit interface

## 🏗️ Architecture

```
User Query → Embedding → Vector Search (FAISS) → Retrieve Relevant Chunks → 
LLM (Groq) + Context → Generate Answer → Display with Sources
```

**Tech Stack:**
- **Frontend:** Streamlit
- **LLM Framework:** LangChain
- **Vector Database:** FAISS
- **Embeddings:** HuggingFace Sentence Transformers
- **LLM API:** Groq (Mixtral-8x7b)
- **PDF Processing:** PyPDF

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Groq API key ([Get it free here](https://console.groq.com))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/abhigyaabs2/AI-Study-Partner.git
cd AI-Study-Partner
```

2. **Create virtual environment**
```bash
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
use untitled(3).ipynb
```

4. **Run the application**
```bash
streamlit run study.py
```

5. **Open your browser**
   - The app will automatically open at `http://localhost:8501`

## 📖 Usage

1. **Enter API Key:** Add your Groq API key in the sidebar
2. **Upload PDFs:** Select one or more PDF files (syllabus, notes, textbooks)
3. **Process Documents:** Click "Process PDFs" to create the knowledge base
4. **Ask Questions:** Start chatting with your AI study partner!

### Example Questions

```
✅ "What are the main topics covered in this syllabus?"
✅ "Explain the concept of neural networks in simple terms"
✅ "What are the prerequisites for this course?"
✅ "Summarize chapter 3 on data structures"
✅ "Compare supervised and unsupervised learning"
✅ "What assignment weightage is mentioned?"
```

## 🛠️ Configuration

The app uses the following default settings:

- **LLM Model:** Mixtral-8x7b-32768 (via Groq)
- **Temperature:** 0.3 (for focused, factual responses)
- **Chunk Size:** 1000 characters
- **Chunk Overlap:** 200 characters
- **Retrieval:** Top 3 most relevant chunks
- **Embeddings:** all-MiniLM-L6-v2

## 📁 Project Structure

```
ai-study-partner/
│
├── app.py                 # Main Streamlit application
├── README.md             # Project documentation
└── .gitignore            # Git ignore file
```

## 🔧 Technologies Used

| Technology | Purpose |
|------------|---------|
| **Streamlit** | Web interface and UI |
| **LangChain** | LLM application framework |
| **Groq API** | Fast LLM inference |
| **FAISS** | Vector similarity search |
| **HuggingFace** | Sentence embeddings |
| **PyPDF** | PDF text extraction |

## 💡 How It Works

### 1. Document Processing
- PDFs are loaded and text is extracted
- Text is split into manageable chunks (1000 chars)
- Overlapping ensures context preservation

### 2. Vector Embedding
- Chunks are converted to embeddings using Sentence Transformers
- Embeddings capture semantic meaning of text
- Stored in FAISS for efficient retrieval

### 3. Query Processing
- User question is embedded using the same model
- Similarity search finds most relevant chunks
- Top 3 chunks are retrieved as context

### 4. Answer Generation
- Retrieved chunks + question sent to Groq LLM
- Mixtral model generates contextual answer
- Sources are displayed for transparency

### 5. Conversation Memory
- Chat history maintained in session
- Context passed for follow-up questions
- Natural conversational flow

## 🎯 Use Cases

- **Students:** Study for exams, understand complex topics
- **Teachers:** Quick reference for course materials
- **Researchers:** Extract information from papers
- **Professionals:** Learn from technical documentation

## 🔒 Privacy & Security

- All processing happens in your local environment
- PDFs are temporarily stored only during processing
- No data is sent to external servers except API calls
- API key is never stored permanently

## 🐛 Troubleshooting

**Issue: Module not found**
```bash
# Ensure virtual environment is activated
```

**Issue: Invalid API key**
- Verify your Groq API key is correct
- Check API usage limits at console.groq.com

**Issue: PDF not processing**
- Ensure PDF contains text (not scanned images)
- Try with smaller files first
- Check PDF is not password-protected

**Issue: Slow responses**
- Normal for large documents on first processing
- Subsequent queries are faster
- Consider splitting very large PDFs

## 🚀 Future Enhancements

- [ ] Support for DOCX and TXT files
- [ ] Chat history export (JSON/CSV)
- [ ] Quiz generation from syllabus
- [ ] Flashcard creation
- [ ] Study session analytics
- [ ] Multi-language support
- [ ] Voice input/output
- [ ] Mobile-responsive design
- [ ] Custom model selection

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [LangChain](https://langchain.com/)
- Powered by [Groq](https://groq.com/)
- UI with [Streamlit](https://streamlit.io/)
- Embeddings by [HuggingFace](https://huggingface.co/)

---

⭐ If you find this project helpful, please consider giving it a star!

**Made with ❤️ and Python**
