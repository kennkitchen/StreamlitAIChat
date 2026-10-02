import sys
import streamlit as st
import ollama
from modules.yolama import OllamaConversationManager as yolama

def fetch_available_models() -> list:
    """Queries the local Ollama server for a list of available models."""
    response = ollama.list()

    models_data = response.models if hasattr(response, 'models') else response.get('models', [])

    model_names = []
    for m in models_data:
        if hasattr(m, 'model'):
            model_names.append(m.model)
        elif isinstance(m, dict):
            name = m.get('model') or m.get('name')
            if name:
                model_names.append(name)

    return model_names

def load_models():
    try:
        models = fetch_available_models()
    except Exception as e:
        print("SWTW")
        return

    print(models)



def main():
    st.title("🦜🔗 Ye Olde Local AI Thingy")

    # load_models()
    yoinstance = yolama()

    with st.form("my_form"):
        text = st.text_area(
            "Enter text:",
            "What are the three key pieces of advice for learning how to code?",
        )
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.info(yoinstance.generate_response(text))



if __name__ == "__main__":
    main()


