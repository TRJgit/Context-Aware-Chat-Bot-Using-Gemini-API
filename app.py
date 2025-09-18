import streamlit as st
import google.generativeai as genai
import PyPDF2
import docx

st.set_page_config(page_title="Gemini Chat", page_icon="✨")
st.title("✨ Gemini Chat")
st.markdown("Chat with your documents using Google Gemini models.")

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
    st.session_state.model = "gemini-1.5-flash-latest"
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7
if "top_p" not in st.session_state:
    st.session_state.top_p = 0.9
if "max_tokens" not in st.session_state:
    st.session_state.max_tokens = 512
if "file_content" not in st.session_state:
    st.session_state.file_content = None

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("Model Configuration")

    gemini_api_key = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="Enter API key",
        help="Get your API key from https://aistudio.google.com/apikey"
    )
    if gemini_api_key:
        genai.configure(api_key=gemini_api_key)
        st.success("Gemini API Key saved!")

    gemini_models = [
        "gemini-1.5-flash-latest",
        "gemini-1.5-pro-latest",
        "gemini-pro"
    ]
    st.session_state.model = st.selectbox("Choose your Gemini model", gemini_models, key="model_selector_gemini")

    st.subheader("Model Parameters")
    st.session_state.temperature = st.slider("Temperature", 0.0, 1.0, st.session_state.temperature, 0.01)
    st.session_state.top_p = st.slider("Top P", 0.0, 1.0, st.session_state.top_p, 0.01)
    st.session_state.max_tokens = st.slider("Max Tokens", 64, 8192, st.session_state.max_tokens, 64)

    st.header("Upload a File")
    uploaded_file = st.file_uploader("Upload a document for context.", type=['pdf', 'docx', 'txt', 'md'])

    if uploaded_file is not None:
        file_name = uploaded_file.name
        if file_name.endswith('.pdf'):
            st.session_state.file_content = read_pdf(uploaded_file)
        elif file_name.endswith('.docx'):
            st.session_state.file_content = read_docx(uploaded_file)
        else:
            st.session_state.file_content = read_txt(uploaded_file)

        if "Error" in str(st.session_state.file_content):
            st.error(st.session_state.file_content)
            st.session_state.file_content = None
        else:
            st.success(f"Successfully processed '{file_name}'!")

    st.subheader("Chat Management")
    def clear_chat_and_context():
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
        st.session_state.file_content = None

    st.button('Clear Chat History & File', on_click=clear_chat_and_context)

# --- Main Chat Interface ---
def gemini_res_generator(prompt_with_context, model_name):
    """Stream response from Gemini model."""
    model = genai.GenerativeModel(model_name)
    generation_config = genai.GenerationConfig(
        temperature=st.session_state.temperature,
        top_p=st.session_state.top_p,
        max_output_tokens=st.session_state.max_tokens
    )
    stream = model.generate_content(prompt_with_context, generation_config=generation_config, stream=True)
    for chunk in stream:
        yield chunk.text

for msg in st.session_state.messages:
    avatar = "🧑‍💻" if msg["role"] == "user" else "✨"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    # Prepare the prompt for the model, including context if a file is uploaded
    final_prompt = prompt
    if st.session_state.file_content:
        final_prompt = f"""Using the context provided below, answer the following question.
---
Context:
{st.session_state.file_content}
---
Question:
{prompt}
"""
    # Generate and display the assistant's response
    full_response = ""
    with st.chat_message("assistant", avatar="✨"):
        message_placeholder = st.empty()
        try:
            if not gemini_api_key:
                st.error("Please enter your Gemini API Key in the sidebar to continue.")
            else:
                generator = gemini_res_generator(final_prompt, st.session_state.model)
                for chunk in generator:
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
            full_response = f"Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": full_response})