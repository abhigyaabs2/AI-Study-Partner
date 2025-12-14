import streamlit as st
import requests
import json
from PyPDF2 import PdfReader
import hashlib
import pickle
import os

# Page config
st.set_page_config(
    page_title="AI Study Partner",
    page_icon="📚",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .bot-message {
        background-color: #f5f5f5;
    }
    .message-content {
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'document_chunks' not in st.session_state:
    st.session_state.document_chunks = []
if 'processed_files' not in st.session_state:
    st.session_state.processed_files = []

# Title
st.title("📚 AI Study Partner")
st.markdown("*Your personal AI tutor trained on your syllabus*")

# Helper Functions
def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF"""
    try:
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page_num, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()
            text += f"\n\n[Page {page_num + 1}]\n{page_text}"
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return None

def chunk_text(text, chunk_size=1000, overlap=200):
    """Split text into overlapping chunks"""
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        
        # Try to break at sentence boundary
        if end < text_length:
            last_period = chunk.rfind('.')
            last_newline = chunk.rfind('\n')
            break_point = max(last_period, last_newline)
            if break_point > chunk_size * 0.5:  # Only break if we're past halfway
                end = start + break_point + 1
                chunk = text[start:end]
        
        chunks.append({
            'text': chunk.strip(),
            'start': start,
            'end': end
        })
        
        start = end - overlap
    
    return chunks

def find_relevant_chunks(query, chunks, top_k=3):
    """Simple relevance search based on keyword matching"""
    query_words = set(query.lower().split())
    
    scored_chunks = []
    for chunk in chunks:
        chunk_words = set(chunk['text'].lower().split())
        # Calculate overlap score
        overlap = len(query_words & chunk_words)
        if overlap > 0:
            scored_chunks.append((chunk, overlap))
    
    # Sort by score and return top k
    scored_chunks.sort(key=lambda x: x[1], reverse=True)
    return [chunk for chunk, score in scored_chunks[:top_k]]

def call_groq_api(api_key, messages, temperature=0.3):
    """Call Groq API directly without langchain"""
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 2000
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Key input
    groq_api_key = st.text_input("Enter Groq API Key:", type="password")
    st.markdown("[Get your Groq API key](https://console.groq.com/keys)")
    
    st.divider()
    
    # File uploader
    st.header("📄 Upload Syllabus PDFs")
    uploaded_files = st.file_uploader(
        "Upload your study materials",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload PDF files containing your syllabus, notes, or study materials"
    )
    
    # Process button
    process_btn = st.button("🔄 Process Documents", type="primary", use_container_width=True)
    
    if st.session_state.processed_files:
        st.success(f"✅ {len(st.session_state.processed_files)} file(s) processed")
        with st.expander("View processed files"):
            for file in st.session_state.processed_files:
                st.write(f"📄 {file}")
    
    st.divider()
    
    # Settings
    st.header("🎯 Settings")
    temperature = st.slider("Response Creativity:", 0.0, 1.0, 0.3, 0.1)
    chunk_size = st.slider("Chunk Size:", 500, 2000, 1000, 100)
    top_k = st.slider("Relevant Chunks:", 2, 5, 3, 1)
    
    st.divider()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()
    
    st.divider()
    st.markdown("### 💡 Tips")
    st.info("""
    - Upload multiple PDFs for comprehensive coverage
    - Ask specific questions about topics
    - Request explanations, summaries, or examples
    - Use follow-up questions for deeper understanding
    """)

# Process documents when button is clicked
if process_btn:
    if not groq_api_key:
        st.error("Please enter your Groq API key!")
    elif not uploaded_files:
        st.error("Please upload at least one PDF file!")
    else:
        with st.spinner("📖 Processing your documents..."):
            all_chunks = []
            processed_names = []
            
            for uploaded_file in uploaded_files:
                # Extract text from PDF
                text = extract_text_from_pdf(uploaded_file)
                if text:
                    # Chunk the text
                    chunks = chunk_text(text, chunk_size=chunk_size)
                    for chunk in chunks:
                        chunk['source'] = uploaded_file.name
                    all_chunks.extend(chunks)
                    processed_names.append(uploaded_file.name)
            
            if all_chunks:
                st.session_state.document_chunks = all_chunks
                st.session_state.processed_files = processed_names
                st.session_state.chat_history = []
                st.success(f"✅ Successfully processed {len(processed_names)} file(s) with {len(all_chunks)} chunks!")
                st.rerun()

# Main chat interface
st.markdown("---")

# Display chat history
chat_container = st.container()
with chat_container:
    for i, message in enumerate(st.session_state.chat_history):
        if message['role'] == 'user':
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>🧑 You:</strong>
                <div class="message-content">{message['content']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message bot-message">
                <strong>🤖 AI Study Partner:</strong>
                <div class="message-content">{message['content']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Show sources if available
            if 'sources' in message and message['sources']:
                with st.expander("📚 View Sources"):
                    for idx, source in enumerate(message['sources'], 1):
                        st.markdown(f"**Source {idx}:** {source['source']}")
                        st.text(source['text'][:400] + "...")
                        st.divider()

# Chat input
if st.session_state.document_chunks and groq_api_key:
    user_question = st.chat_input("Ask a question about your syllabus...")
    
    if user_question:
        # Add user message to chat history
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_question
        })
        
        # Get response
        with st.spinner("🤔 Thinking..."):
            try:
                # Find relevant chunks
                relevant_chunks = find_relevant_chunks(
                    user_question, 
                    st.session_state.document_chunks, 
                    top_k=top_k
                )
                
                # Build context from relevant chunks
                context = "\n\n".join([
                    f"[From {chunk['source']}]\n{chunk['text']}" 
                    for chunk in relevant_chunks
                ])
                
                # Build chat history for context
                recent_history = st.session_state.chat_history[-6:]  # Last 3 exchanges
                history_text = "\n".join([
                    f"{msg['role'].title()}: {msg['content']}" 
                    for msg in recent_history[:-1]  # Exclude current question
                ])
                
                # Create messages for API
                system_message = """You are a helpful AI study partner. Use the provided context from the user's study materials to answer their questions accurately. 
                
If the answer is not in the context, say so honestly. When possible, explain concepts clearly and provide examples.

Remember previous questions in the conversation to provide coherent follow-up answers."""
                
                messages = [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": f"""Context from study materials:
{context}

Previous conversation:
{history_text}

Current question: {user_question}

Please answer based on the context provided."""}
                ]
                
                # Call Groq API
                answer = call_groq_api(groq_api_key, messages, temperature)
                
                if answer:
                    # Add assistant message to chat history
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': answer,
                        'sources': relevant_chunks
                    })
                    
                    st.rerun()
                
            except Exception as e:
                st.error(f"Error generating response: {str(e)}")
else:
    if not groq_api_key:
        st.warning("👈 Please enter your Groq API key in the sidebar!")
    elif not st.session_state.document_chunks:
        st.info("👈 Please upload PDF files and click 'Process Documents' to start chatting!")
    
    # Example questions
    st.markdown("### 💭 Example Questions You Can Ask:")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        - Explain the concept of [topic]
        - What are the key points about [subject]?
        - Summarize chapter [X]
        - Give me examples of [concept]
        """)
    
    with col2:
        st.markdown("""
        - What's the difference between [A] and [B]?
        - How does [process] work?
        - List the main topics in [chapter]
        - Quiz me on [subject]
        """)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Built with Streamlit and Groq AI | Your personal AI study companion 📚</p>
</div>
""", unsafe_allow_html=True)