from modules.engine import AIEngine
import ollama

class OllamaConversationManager:
    """
    A class to manage interactions with a local Ollama instance,
    handling model selection and conversation state.
    """

    def __init__(self):
        self.messages = []  # Stores the conversation history for context
        self.AIEngine = AIEngine()
        self.model_name = "gemma4:latest" # AIEngine.get_last_model()

    def set_model(self, model: str):
        """Sets the active model and resets conversation history."""
        self.model_name = model
        self.messages = []


    def generate_response(self, user_input: str) -> str:
        """Generates an assistant response and updates conversation history."""
        if not self.model_name:
            raise RuntimeError("No model selected.")

        if not user_input:
            return ""

        self.messages.append({'role': 'user', 'content': user_input})

        response_content = ""
        stream = ollama.chat(
            model=self.model_name,
            messages=self.messages,
            stream=True
        )

        for chunk in stream:
            token = chunk['message']['content']
            response_content += token

        self.messages.append({'role': 'assistant', 'content': response_content})
        return response_content