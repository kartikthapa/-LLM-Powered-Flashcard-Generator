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

```
### 2. Install Dependencies
```bash
pip install -r requirements.txt

```
### 3. Run the App
```bash
streamlit run app.py
 ```

## Sample Flashcards Output

Here are some example flashcards generated from an input on the topic **Photosynthesis**:

| Question                                                         | Answer                                                                                     |
|------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| What is photosynthesis?                                          | Photosynthesis is the process by which plants convert light energy into chemical energy.  |
| What are the main stages of photosynthesis?                      | The light-dependent reactions and the Calvin cycle are the two main stages.               |
| What is the function of chlorophyll in photosynthesis?           | Chlorophyll absorbs sunlight and initiates the light reactions in the chloroplast.        |
| Where does the Calvin cycle occur?                               | It takes place in the stroma of chloroplasts.                                              |
| Why is photosynthesis important for life on Earth?               | It produces oxygen and glucose, supporting food chains and atmospheric balance.           |

## Sample Execution 

- **Input Type**: Paste Input 
- **Topic**: History
- **Flashcards Generated**: 15 
- **Export Formats**: [View CSV](sample_output/flashcards_history.csv) | [View Anki TXT](sample_output/anki_flashcards_history.txt)


