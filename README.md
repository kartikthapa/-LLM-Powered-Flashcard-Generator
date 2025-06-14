# -LLM-Powered-Flashcard-Generator
This is a Python + Streamlit-based app that uses a large language model (`Flan-T5`) to automatically generate Q&A-style flashcards from educational content. It supports text input, PDF uploads, and TXT files, and provides downloads in both CSV and Anki formats.

-------------------

## Features

-  Generates 10–15 flashcards using `google/flan-t5-large`
-  Smart + fallback question generation (always produces output)
-  Supports pasted text, PDFs, and TXT files
-  Downloads in CSV and Anki (TXT) format
-  Streamlit UI – clean, minimal, and easy to use

-------------------

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/kartikthapa/LLM-Powered-Flashcard-Generator.git
cd LLM-Powered-Flashcard-Generator
