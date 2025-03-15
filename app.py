import streamlit as st

# ✅ MUST be the first Streamlit command
st.set_page_config(
    page_title="Jaun Elia GPT",
    page_icon="✍️",
    layout="wide"
)

import os
from dotenv import load_dotenv

# ✅ Ensure this is AFTER `st.set_page_config()`
try:
    import google.generativeai as genai
except ImportError:
    st.error("Please install google-generativeai: pip install google-generativeai")
    st.stop()

# Load API Key from .env
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Google AI API
if API_KEY:
    genai.configure(api_key=API_KEY)
    
else:
    st.error("❌ API Key not found. Please set it in Streamlit secrets or .env file.")
    st.stop()





# Sidebar content
with st.sidebar:
     # Replace with your logo
    st.title("Jaun Elia GPT")
    st.markdown("---")
    
    # About section
    st.subheader("About")
    st.write("An AI poetry assistant specializing in Urdu poetry written in Roman script.")
    
    # Options
    st.subheader("Poetry Options")
    poetry_style = st.selectbox(
        "Poetry Style",
        ["Ghazal", "Nazm", "Rubai", "Free Verse"]
    )
    
    poetry_mood = st.selectbox(
        "Mood",
        ["Romantic", "Philosophical", "Melancholic", "Hopeful", "Nostalgic"]
    )
    
    poetry_length = st.slider(
        "Number of Lines",
        min_value=2,
        max_value=12,
        value=6,
        step=2
    )
    
    st.markdown("---")
    st.caption("© 2025 Jaun Elia GPT by Khalid Hussain")
    
    # Language selection
    language = st.radio(
        "Language for Instructions",
        ["English", "Urdu (Roman)"]
    )

# Main content area
st.title("Jaun Elia GPT - Poetry Generator 📝")
st.markdown("Generate beautiful Urdu poetry in Roman script on any topic of your choice.")

# Example prompts
with st.expander("💡 Example Prompts", expanded=False):
    st.markdown("""
    - Mohabbat (Love)
    - Dosti ke rang (Colors of friendship)
    - Tanhayi mein yaad teri (Remembering you in solitude)
    - Zindagi ka safar (Life's journey)
    - Raat ka andhera (Darkness of night)
    """)

# Input options
input_type = st.radio(
    "Select input type",
    ["Topic/Theme", "First Line", "Emotion", "Complete a Verse"]
)

# User input
placeholder_text = {
    "Topic/Theme": "Enter a topic (e.g., love, friendship, nature)",
    "First Line": "Enter the first line of poetry",
    "Emotion": "Enter an emotion (e.g., happiness, sadness, longing)",
    "Complete a Verse": "Enter an incomplete verse to complete"
}

user_input = st.text_area(
    "Your Input:",
    height=100,
    placeholder=placeholder_text[input_type]
)

# Advanced options
with st.expander("Advanced Options", expanded=False):
    model_version = st.selectbox(
        "Model Version",
        ["gemini-2.0-flash", "gemini-2.0-pro"],
        index=0
    )
    
    temperature = st.slider(
        "Creativity Level",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Higher values make output more creative, lower values make it more deterministic"
    )
    
    include_translation = st.checkbox("Include English Translation", value=True)
    
    include_explanation = st.checkbox("Include Cultural Context", value=False)

# Generate button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    generate_button = st.button("✨ Generate Poetry", type="primary", use_container_width=True)

# Save poetry feature
def save_poetry(poetry):
    st.session_state.saved_poems = st.session_state.get('saved_poems', []) + [poetry]
    st.success("Poetry saved to your collection!")

# Initialize or get history
if 'history' not in st.session_state:
    st.session_state.history = []

# Generate poetry
if generate_button and user_input:
    with st.spinner("Crafting poetry..."):
        try:
            # Construct prompt based on user selections
            prompt_template = f"""You are John Alya, an AI poetry assistant specializing in Urdu poetry, responding in Roman Urdu (ABC format). 
            
            # Task
            Generate {poetry_length} lines of {poetry_style} with a {poetry_mood} mood based on the user's {input_type.lower()}: "{user_input}".
            
            # Output Format
            - Title: Give the poetry a meaningful title
            - Poetry: Write {poetry_length} lines of beautiful Urdu poetry in Roman script
            {'- Translation: Provide an English translation of the poetry' if include_translation else ''}
            {'- Context: Briefly explain any cultural references or deeper meanings' if include_explanation else ''}
            
            # Style Guidelines
            - Use authentic Urdu poetic devices (metaphors, similes, etc.)
            - Maintain proper Urdu grammar in Roman script
            - Create depth and emotional resonance
            - Avoid clichés and superficial expressions
            - Ensure the poetry flows naturally and has rhythm
            
            # Response Structure
            Format your response clearly with headings for each section.
            """
            
            # Select model based on user choice
            model = genai.GenerativeModel(
                model_version,
                generation_config={"temperature": temperature}
            )
            
            # Generate response
            response = model.generate_content(prompt_template)
            
            # Display response
            st.markdown("## Generated Poetry")
            output_container = st.container(border=True)
            with output_container:
                st.markdown(response.text)
                
                # Add to history
                st.session_state.history.append({
                    "input": user_input,
                    "output": response.text,
                    "style": poetry_style,
                    "mood": poetry_mood
                })
                
                # Save option
                if st.button("💾 Save to Collection"):
                    save_poetry(response.text)
                
                # Copy option
                st.button("📋 Copy to Clipboard", on_click=lambda: st.write("Poetry copied to clipboard!"))
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
else:
    if not user_input and generate_button:
        st.warning("Please enter a topic or a line for poetry generation.")

# History tab
if st.session_state.get('history', []):
    with st.expander("📜 Your Poetry History", expanded=False):
        for i, item in enumerate(st.session_state.history):
            with st.container(border=True):
                st.write(f"**Input:** {item['input']}")
                st.write(f"**Style:** {item['style']} | **Mood:** {item['mood']}")
                st.markdown(item['output'])
                st.button(f"Delete #{i+1}", key=f"delete_{i}", on_click=lambda i=i: st.session_state.history.pop(i))

# Collection tab
if st.session_state.get('saved_poems', []):
    with st.expander("📚 Your Poetry Collection", expanded=False):
        for i, poem in enumerate(st.session_state.saved_poems):
            with st.container(border=True):
                st.markdown(poem)
                col1, col2 = st.columns(2)
                with col1:
                    st.button(f"Export #{i+1}", key=f"export_{i}")
                with col2:
                    st.button(f"Remove #{i+1}", key=f"remove_{i}", on_click=lambda i=i: st.session_state.saved_poems.pop(i))

# Footer
st.markdown("---")
st.caption("Jaun Elia GPT - Create beautiful Urdu poetry with the power of AI by Khalid Husssain")
