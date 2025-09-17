# main.py

import os
from dotenv import load_dotenv
from aura_core.ai_core import AuraAICore

def main():
    # Load the environment variables from the .env file
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        print("🔴 Error: GOOGLE_API_KEY not found. Please create a .env file.")
        return

    # Initialize our AI core
    ai_core = AuraAICore(api_key=api_key)
    print("✨ Aura AI Core Initialized ✨")
    print("-" * 30)

    # --- 1. Test the Direct Command Generation ---
    print("\n🧪 Testing Direct Command Generation...")
    request1 = "delete all the files with ai in its name"
    command1 = ai_core.get_direct_command(request1)
    print(f"   🗣️ User: '{request1}'")
    print(f"   🤖 Aura's Command: {command1}")
    
    request2 = "find all text files in my home directory"
    command2 = ai_core.get_direct_command(request2)
    print(f"\n   🗣️ User: '{request2}'")
    print(f"   🤖 Aura's Command: {command2}")
    print("-" * 30)

    print("\n🧪 Testing Socratic Tutor (type 'exit' to end)")
    ai_core.reset_conversation()
    
    # Start the conversation
    initial_prompt = "I need to clean up my downloads folder."
    print(f"   🗣️ User: {initial_prompt}")
    
    # Get the AI's first question
    ai_question = ai_core.start_socratic_dialogue(initial_prompt)
    print(f"   🤖 Aura: {ai_question}")

    # Enter an interactive loop to continue the conversation
    while True:
        user_response = input("   ➡️ Your Response: ")
        if user_response.lower() == 'exit':
            break
        
        ai_question = ai_core.start_socratic_dialogue(user_response)
        print(f"   🤖 Aura: {ai_question}")


if __name__ == "__main__":
    main()