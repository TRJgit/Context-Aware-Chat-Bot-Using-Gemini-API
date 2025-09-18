# Local LLM Chat UI

A user-friendly Streamlit-based chat interface that allows you to interact with local language models and chat with your documents. This application also features a separate chat page for interacting with Google's Gemini models.

## 🚀 Features

  * **Local Model Integration:** Seamlessly connect to and switch between various local language models running via Ollama.
  * **Document Chat:** Upload your documents (PDF, DOCX, TXT, MD) and ask questions about their content.
  * **Gemini Chat:** A dedicated page to chat with Google's Gemini models, with configurable parameters like temperature, top-p, and max tokens.
  * **Chat History:** Your conversation is saved within the session.
  * **Customizable UI:** The theme of the application can be easily customized through the `config.toml` file.
  * **Clear Chat and Context:** A simple button to clear the chat history and the uploaded document's context.

## 🖼️ Demo

\*\*

## 🛠️ How it Works

The application is built with **Streamlit** and leverages the **Ollama** library to interact with local language models. For document processing, it uses **PyPDF2** and **python-docx**. The Gemini chat functionality is powered by the **google-generativeai** library.

The main page, **Local Chat**, allows you to select a local model from the ones available in your Ollama instance. You can upload a document, and its content will be injected as context into your prompts, enabling you to "chat" with your document.

The **Gemini Chat** page provides an interface to interact with the Gemini API. You can enter your API key, choose a Gemini model, and adjust various generation parameters to tailor the model's responses to your needs.

## ⚙️ Installation

To get started with this application, follow these steps:

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/TRJgit/Local-LLM-Chat-UI.git
    cd Local-LLM-Chat-UI
    ```

2.  **Install the dependencies:**
    Make sure you have Python 3.8+ installed. Then, install the required packages using pip:

    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Streamlit application:**

    ```bash
    streamlit run Local_Chat.py
    ```

    The application will open in your default web browser.

## 📖 Usage

### Local Chat

1.  **Select a model:** Choose a local model from the dropdown menu in the sidebar.
2.  **Upload a document (optional):** If you want to chat with a document, upload a file using the file uploader in the sidebar. The supported file types are PDF, DOCX, TXT, and MD.
3.  **Start chatting:** Type your questions in the chat input box at the bottom of the page.
4.  **Clear chat and context:** Click the "Clear Chat History & File" button in the sidebar to reset the conversation and remove the uploaded document's content.

### Gemini Chat

1.  **Navigate to the Gemini Chat page:** Use the sidebar to go to the "Gemini Chat" page.
2.  **Enter your API key:** Provide your Gemini API key in the text input field in the sidebar. You can get your key from the [Google AI Studio](https://aistudio.google.com/apikey).
3.  **Choose a model:** Select one of the available Gemini models from the dropdown.
4.  **Adjust parameters (optional):** You can fine-tune the model's behavior by adjusting the temperature, top-p, and max tokens sliders in the sidebar.
5.  **Start chatting:** Use the chat input to ask your questions.
6.  **Clear chat history:** Click the "Clear Chat History" button to start a new conversation.

## 🎨 Configuration

You can customize the application's theme by modifying the `.streamlit/config.toml` file. The file allows you to change the primary color, background colors, text color, and font.

```toml
[theme]
# The primary accent color for interactive elements.
primaryColor = "#db3434ff"

# Background color for the main content area.
backgroundColor = "#212121"

# Background color for sidebar and most interactive widgets.
secondaryBackgroundColor = "#191919"

# Color of text.
textColor = "#FAFAFA"

# Font family for all text in the app.
font = "sans serif"
```

## 📂 Project Structure

```
├── .streamlit/
│   └── config.toml      # Streamlit theme configuration
├── pages/
│   └── 1_Gemini_Chat.py # The Gemini chat page
├── .gitignore           # Files to be ignored by Git
├── Local_Chat.py        # The main application file
├── README.md            # README 
└── requirements.txt     # Project dependencies
```

## 📦 Dependencies

The main dependencies of this project are:

  * **streamlit:** The web application framework.
  * **ollama:** To interact with local language models.
  * **PyPDF2:** For reading PDF files.
  * **python-docx:** For reading DOCX files.
  * **google-generativeai:** For the Gemini chat functionality.

