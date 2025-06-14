import streamlit as st
from transformers import pipeline
import pdfplumber
import pandas as pd
import re

@st.cache_resource
def load_model():
    try:
        return pipeline("text2text-generation", model="google/flan-t5-large", tokenizer="google/flan-t5-large")
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

model = load_model()

def extract_text_from_pdf(file):
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        st.error(f"Error extracting PDF: {e}")
        return ""

def generate_flashcards_smart(text, subject="General"):
    flashcards = []
    sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 15]

    question_templates = [
        "What is {}?",
        "Define {}.",
        "Explain {}.",
        "What does {} mean?",
        "How would you describe {}?",
        "What can you tell me about {}?"
    ]
    
    for sentence in sentences[:25]:
        if len(flashcards) >= 15:
            break
        sentence = sentence.strip()
        if len(sentence) < 20:
            continue
        question = generate_single_question(sentence, subject)
        if question and question != sentence:
            flashcards.append({"Question": question, "Answer": sentence})
        else:
            key_terms = extract_key_terms(sentence)
            if key_terms:
                template = question_templates[len(flashcards) % len(question_templates)]
                question = template.format(key_terms[0])
                flashcards.append({"Question": question, "Answer": sentence})

    return flashcards

def generate_single_question(sentence, subject):
    if not model:
        return None
    prompts = [
        f"What question does this answer: {sentence[:150]}",
        f"Turn into a question: {sentence[:150]}",
        f"Question for: {sentence[:150]}"
    ]
    for prompt in prompts:
        try:
            result = model(prompt, max_length=80, do_sample=False, num_beams=2)[0]['generated_text']
            result = result.replace(prompt, "").strip()
            if result and len(result) > 8 and len(result) < 200:
                if not result.endswith('?'):
                    result += '?'
                return result
        except Exception:
            continue
    return None

def extract_key_terms(sentence):
    common_words = {'the', 'is', 'are', 'was', 'were', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an'}
    words = sentence.split()
    key_terms = []
    for word in words:
        word = re.sub(r'[^\w\s]', '', word)
        if len(word) > 3 and word.lower() not in common_words and (word[0].isupper() or len(word) > 6):
            key_terms.append(word)
    return key_terms[:3]

def create_basic_flashcards(text, subject="General"):
    sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 20]
    flashcards = []
    question_patterns = [
        "What is the main concept discussed in this statement?",
        "According to the text, what information is provided?",
        "What does this statement explain?",
        "What key information is mentioned here?",
        "What is described in this part of the text?",
        "Can you summarize the key idea here?",
        "What fact is presented in this statement?",
        "What scientific point is being made?",
        "What does this tell us?",
        "Why is this detail important?",
        "How does this relate to the topic?",
        "What insight is offered here?",
        "What conclusion is being drawn?",
        "What aspect of the topic is discussed here?",
        "How is this idea explained?"
    ]
    for i, sentence in enumerate(sentences[:15]):
        question = question_patterns[i % len(question_patterns)]
        flashcards.append({"Question": question, "Answer": sentence.strip()})
    return flashcards

#---ANKI---#
def create_anki_format(flashcards, subject="General"):
    anki_content = []
    for card in flashcards:
        question = card['Question'].replace(';', '&#59;').replace('"', '&quot;')
        answer = card['Answer'].replace(';', '&#59;').replace('"', '&quot;')
        anki_line = f'"{question}";"{answer}";"{subject.lower()}"'
        anki_content.append(anki_line)
    return '\n'.join(anki_content)

def create_anki_apkg_info(subject="General"):
    info = f"""
    📋 **Anki Import Instructions:**
    
    1. Open Anki and go to **File → Import**
    2. Select the downloaded .txt file
    3. Set the field separator to **Semicolon**
    4. Map fields as: **Field 1 → Front**, **Field 2 → Back**, **Field 3 → Tags**
    5. Choose your target deck or create a new one
    6. Click **Import**
    
    **Note:** Your flashcards will be tagged with "{subject.lower()}" for easy organization.
    """
    return info

st.title("📚 LLM Powered Flashcard Generator")
st.write("Upload educational content and generate flashcards for Anki or other platforms.")

debug_mode = st.checkbox("Enable Debug Mode")
subject = st.selectbox("Select Subject (optional)", ["General", "Biology", "History", "Computer Science", "Physics", "Math"])
input_type = st.radio("Choose input method:", ["Paste text", "Upload .pdf", "Upload .txt"])
input_text = ""

if input_type == "Paste text":
    input_text = st.text_area("Paste educational content here", height=200)
elif input_type == "Upload .pdf":
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    if uploaded_file:
        with st.spinner("Extracting text..."):
            input_text = extract_text_from_pdf(uploaded_file)
elif input_type == "Upload .txt":
    uploaded_file = st.file_uploader("Upload a TXT file", type="txt")
    if uploaded_file:
        try:
            input_text = uploaded_file.read().decode("utf-8")
        except Exception as e:
            st.error(f"Error reading file: {e}")

#---UI---#
if st.button("⚡ Generate Flashcards"):
    if not input_text.strip():
        st.error("Please provide some content.")
    else:
        with st.spinner("Generating flashcards..."):
            flashcards = generate_flashcards_smart(input_text, subject)
            if len(flashcards) < 3:
                basic_cards = create_basic_flashcards(input_text, subject)
                flashcards.extend(basic_cards)
                seen = set()
                unique_flashcards = []
                for card in flashcards:
                    if card['Answer'] not in seen:
                        seen.add(card['Answer'])
                        unique_flashcards.append(card)
                flashcards = unique_flashcards[:5]

            if flashcards and isinstance(flashcards, list):
                st.success(f"✅ Generated {len(flashcards)} flashcards!")
                for i, card in enumerate(flashcards, 1):
                    with st.expander(f"Flashcard {i}"):
                        st.write(f"**Q:** {card['Question']}")
                        st.write(f"**A:** {card['Answer']}")
                df = pd.DataFrame(flashcards)
                st.subheader("All Flashcards")
                st.dataframe(df, use_container_width=True)
                st.subheader("📥 Download Options")
                col1, col2 = st.columns(2)
                with col1:
                    csv = df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        "📄 Download as CSV", 
                        data=csv, 
                        file_name=f"flashcards_{subject.lower()}.csv", 
                        mime="text/csv"
                    )
                with col2:
                    anki_content = create_anki_format(flashcards, subject)
                    st.download_button(
                        "🎴 Download for Anki",
                        data=anki_content.encode("utf-8"),
                        file_name=f"anki_flashcards_{subject.lower()}.txt",
                        mime="text/plain"
                    )
                with st.expander("📖 Anki Import Instructions"):
                    st.markdown(create_anki_apkg_info(subject))
            else:
                st.error("Something went wrong. Try different content.")
