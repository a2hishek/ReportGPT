### 📄 `README.md`

# 🧠 ReportGPT – AI-Powered Medical Assistant

**ReportGPT** is a voice-enabled multimodal medical assistant app built with **Streamlit** and powered by **Google's Gemini API** via LangChain. It allows users to upload medical report images, get detailed AI-generated analysis, and chat in English or Hindi for further health explanations — even using voice!

---

## 🔍 Features

- 📷 **Upload medical reports** (JPG/PNG) and get structured, friendly analysis.
- 💬 **Conversational chatbot** that uses report + external knowledge for better responses.
- 🗣️ **Voice input support** using microphone (via SpeechRecognition).
- 🇮🇳 **Supports English and Hindi** toggle for bilingual interaction.
- 🧠 Powered by **Gemini 2.0** LLM and **ChromaDB** for Retrieval-Augmented Generation (RAG).

---

## 🚀 How to Run

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/reportgpt.git
cd reportgpt
````

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file:

```bash
GOOGLE_API_KEY=your_google_api_key
```

Or it will ask for the key interactively.

### 4. Start the app

```bash
streamlit run app.py
```

---

## 🗂️ Project Structure

```
.
├── app.py            # Main Streamlit UI
├── llm.py            # LangChain prompts + Gemini integration
├── recorder.py       # Voice recording & encoding
├── trial.ipynb       # Vector embeddings generation
├── .env              # API key (not committed)
└── README.md         # This file
```

---

## 📦 Dependencies

* `streamlit`
* `langchain`
* `langchain-google-genai`
* `speechrecognition`
* `python-dotenv`
* `chromadb`
* `pyaudio` (for microphone input)

---

## ⚠️ Disclaimer

> This app is for **informational and educational purposes only** and does **not** provide medical advice, diagnosis, or treatment. Always consult a licensed physician for medical concerns.

---

## 🙌 Acknowledgements

* [Google Gemini API](https://ai.google.dev/)
* [LangChain](https://www.langchain.com/)
* [Streamlit](https://streamlit.io/)

