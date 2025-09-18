import ollama
import streamlit as st
import PyPDF2
import docx

# --- Page and Session Configuration ---
st.set_page_config(page_title="Local LLM Chat", page_icon="💬")
st.title("💬 Local LLM Chat")
st.markdown("Chat with your documents using local models.")

# --- File Reading Utilities ---
def read_pdf(file):
    """Reads and extracts text from a PDF file."""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        return f"Error reading PDF file: {e}"

def read_docx(file):
    """Reads and extracts text from a DOCX file."""
    try:
        doc = docx.Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        return f"Error reading DOCX file: {e}"

def read_txt(file):
    """Reads a plain text file."""
    try:
        return file.getvalue().decode("utf-8")
    except Exception as e:
        return f"Error reading text file: {e}"

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
if "model" not in st.session_state:
    st.session_state.model = ""
if "file_content" not in st.session_state:
    st.session_state.file_content = None # Stores the content of the uploaded file

# --- Sidebar ---
with st.sidebar:
    st.header("Model Configuration")
    try:
        local_models = [model['model'] for model in ollama.list().get('models', [])]
        if not local_models:
            st.warning("No local models found. Please ensure Ollama is running.")
            st.stop()
    except Exception as e:
        st.warning(f"Could not connect to Ollama. Error: {e}")
        local_models = []

    st.session_state.model = st.selectbox("Choose your model", local_models, key="model_selector")

    st.header("Upload a File")
    uploaded_file = st.file_uploader("Upload a document for context.", type=['pdf', 'docx', 'txt', 'md'])

    if uploaded_file is not None:
        file_name = uploaded_file.name
        
        # Determine the correct function to read the file
        if file_name.endswith('.pdf'):
            st.session_state.file_content = read_pdf(uploaded_file)
        elif file_name.endswith('.docx'):
            st.session_state.file_content = read_docx(uploaded_file)
        else:
            st.session_state.file_content = read_txt(uploaded_file)

        # Check if reading was successful and update UI
        if "Error" in st.session_state.file_content:
            st.error(st.session_state.file_content)
            st.session_state.file_content = None # Clear content on error
        else:
            st.success(f"Successfully processed '{file_name}'!")

    st.subheader("Chat Management")
    def clear_chat_and_context():
        """Clears chat history and the stored file content."""
        st.session_state.messages = [
            {"role": "assistant", "content": "How may I assist you today?"}
        ]
        st.session_state.file_content = None # Clear the file content

    st.button('Clear Chat History & File', on_click=clear_chat_and_context)

# --- Main Chat Interface ---
def model_res_generator(messages, model_name):
    """Streams response from the Ollama model."""
    stream = ollama.chat(
        model=model_name,
        messages=messages,
        stream=True
    )
    for chunk in stream:
        yield chunk["message"]["content"]

# Display chat messages
for msg in st.session_state.messages:
    avatar = "🧑‍💻" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Handle user input
if prompt := st.chat_input("Ask a question..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    # Prepare messages for the model, creating a temporary copy
    messages_for_model = list(st.session_state.messages)
    
    # If file content exists, inject it as context into the prompt
    if st.session_state.file_content:
        context_prompt = f"""Using the context provided below, answer the following question.
---
Context:
{st.session_state.file_content}
---
Question:
{prompt}
"""
        # Replace the last user message with the augmented prompt
        messages_for_model[-1] = {"role": "user", "content": context_prompt}

    # Generate and display the assistant's response
    full_response = ""
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        try:
            generator = model_res_generator(messages_for_model, st.session_state.model)
            for chunk in generator:
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"An error occurred while generating the response: {e}")
            full_response = f"Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": full_response})