
import google.generativeai as genai
from . import prompts

class AuraAICore:
    """
    The core AI class for Aura. Manages the connection to the LLM
    and holds the logic for different interaction modes.
    """
    def __init__(self, api_key):
        # Configure the generative AI library with the API key
        genai.configure(api_key=api_key)
        
        # Set up the model configuration
        generation_config = {
            "temperature": 0.7,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
        
        # Initialize the model
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash-latest",
            generation_config=generation_config,
        )
        
        # Initialize an empty conversation history for the Socratic tutor
        self.conversation_history = []

    def get_direct_command(self, user_request: str) -> str:
        """
        Gets a direct shell command from a user's request.
        """
        prompt = prompts.SIMPLE_COMMAND_PROMPT.format(user_request=user_request)
        response = self.model.generate_content(prompt)
        # We clean up the response to ensure it's just the command
        return response.text.strip().replace("`", "")

    def start_socratic_dialogue(self, user_request: str) -> str:
        """
        Starts or continues a Socratic dialogue with the user.
        """
        # Add the user's new message to the history
        self.conversation_history.append(f"User: {user_request}")
        
        # Format the history for the prompt
        history_str = "\n".join(self.conversation_history)
        
        # Create the prompt using the history
        prompt = prompts.SOCRATIC_TUTOR_PROMPT.format(history=history_str)
        
        # Generate the AI's next question
        response = self.model.generate_content(prompt)
        ai_response = response.text.strip()
        
        # Add the AI's response to the history to maintain context
        self.conversation_history.append(f"Aura: {ai_response}")
        
        return ai_response

    def reset_conversation(self):
        """Resets the conversation history."""
        self.conversation_history = []