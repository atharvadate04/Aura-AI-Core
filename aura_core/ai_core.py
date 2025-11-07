import google.generativeai as genai
from . import prompts

class AuraAICore:

    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        
        generation_config = {
            "temperature": 0.7,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
        
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash-latest",
            generation_config=generation_config,
        )
        
        self.conversation_history = []
        self.socratic_turn_count = 0
        self.partial_command = ""

    def get_direct_command(self):
        """
        Interactively gets a direct shell command from user input.
        """
        user_request = input("Enter your request: ")
        prompt = prompts.SIMPLE_COMMAND_PROMPT.format(user_request=user_request)
        response = self.model.generate_content(prompt)

        command = response.text.strip().replace("`", "")
        print("\nGenerated command:\n", command)
        return command

    def start_socratic_dialogue(self, user_request: str) -> str:
        """
        Starts or continues a Socratic dialogue with the user.
        Stops after 5-6 interactions or when the final command is ready.
        """

        if self.socratic_turn_count == 0:
            self.conversation_history = []
            self.partial_command = ""

        self.conversation_history.append(f"User: {user_request}")
        history_str = "\n".join(self.conversation_history)
        
        prompt = prompts.SOCRATIC_TUTOR_PROMPT.format(history=history_str, partial_command=self.partial_command)
        
        response = self.model.generate_content(prompt)
        ai_response = response.text.strip()
        self.conversation_history.append(f"Aura: {ai_response}")
        self.socratic_turn_count += 1

        print(f"\n🧩 Step {self.socratic_turn_count}: {ai_response}")

        # Generate partial command after each answer
        partial_prompt = prompts.PARTIAL_COMMAND_PROMPT.format(history=history_str)
        partial_response = self.model.generate_content(partial_prompt)
        self.partial_command = partial_response.text.strip().replace("`", "")

        print("\n🔧 Partial command so far:")
        print(self.partial_command)
        print("\n📘 Explanation:")
        explain_prompt = prompts.EXPLAIN_COMMAND_PROMPT.format(command=self.partial_command)
        explanation = self.model.generate_content(explain_prompt).text.strip()
        print(explanation)

        if self.socratic_turn_count >= 6 or "final command" in ai_response.lower():
            print("\n🎯 Socratic dialogue complete.")
            print("✅ Final command suggestion:\n", self.partial_command)
            self.reset_conversation()

        return ai_response

    def reset_conversation(self):
        """Resets the conversation history."""
        self.conversation_history = []
        self.socratic_turn_count = 0
        self.partial_command = ""
