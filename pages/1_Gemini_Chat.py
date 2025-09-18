import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Gemini Chat", page_icon="💬")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
if "model" not in st.session_state:
    st.session_state.model = ""
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7
if "top_p" not in st.session_state:
    st.session_state.top_p = 0.9
if "max_tokens" not in st.session_state:  
    st.session_state.max_tokens = 512

if st.session_state.temperature >= 1:
    st.warning(
        'Values exceeding 1 produce more creative and random output as well as increased likelihood of hallucination.'
    )
if st.session_state.temperature < 0.1:
    st.warning('Values approaching 0 produce deterministic output. Recommended starting value is 0.7')

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
        st.session_state.gemini_api_key = gemini_api_key
        st.success("Gemini API Key saved!")
    gemini_models = [
        "gemini-1.5-flash-latest",
        "gemini-1.5-pro-latest",
        "gemini-pro"
    ]

    st.session_state.model = st.selectbox("Choose your Gemini model", gemini_models, key="model_selector_gemini")

    # --- Model Parameters Sliders ---
    st.subheader("Model Parameters")

    st.session_state.temperature = st.slider(
        "Temperature",
        min_value=0.0, max_value=1.0,
        value=st.session_state.temperature,
        step=0.01,
        help="Controls creativity. Higher values = more random outputs."
    )

    st.session_state.top_p = st.slider(
        "Top P",
        min_value=0.0, max_value=1.0,
        value=st.session_state.top_p,
        step=0.01,
        help="Controls diversity. Lower values = more focused outputs."
    )

    st.session_state.max_tokens = st.slider(
        "Max Tokens",
        min_value=64, max_value=4096,
        value=st.session_state.max_tokens,
        step=64,
        help="Maximum number of tokens to generate."
    )

    # --- Chat Management ---
    st.subheader("Chat Management")

    def clear_chat_history():
        st.session_state.messages = [
            {"role": "assistant", "content": "How may I assist you today?"}
        ]

    st.button('Clear Chat History', on_click=clear_chat_history)


def gemini_res_generator(messages_with_context, model_name):
    """Stream response from Gemini model."""
    model = genai.GenerativeModel(model_name)

    full_prompt = messages_with_context[-1]['content']

    generation_config = genai.GenerationConfig(
        temperature=st.session_state.temperature,
        top_p=st.session_state.top_p,
        max_output_tokens=st.session_state.max_tokens
    )

    stream = model.generate_content(
        full_prompt,
        generation_config=generation_config,
        stream=True
    )
    for chunk in stream:
        yield chunk.text


# --- Display Messages ---
for msg in st.session_state.messages:
    if msg["role"] == "user":
        avatar = "🧑‍💻"
    elif "gemini" in st.session_state.get("model", "").lower():
        avatar = "✨"
    else:
        avatar = "🤖"

    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# --- Handle User Input ---
if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    # Only use last user prompt
    messages_for_llm = [{"role": "user", "content": prompt}]

    # Stream assistant response
    full_response = ""
    avatar = "✨"  # Always Gemini
    with st.chat_message("assistant", avatar=avatar):
        message_placeholder = st.empty()
        try:
            generator = gemini_res_generator(messages_for_llm, st.session_state.model)

            for chunk in generator:
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
            full_response = f"Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": full_response})
