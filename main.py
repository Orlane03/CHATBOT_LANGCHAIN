# main.py

import config 
from chatbot import get_response

def main():
    print("Chatbot: Bonjour! Comment puis-je vous aider aujourd'hui ?")
    
    while True:
        user_input = input("Vous: ")
        if user_input.lower() in ['quit', 'exit']:
            print("Chatbot: Au revoir!")
            break
        
        response = get_response(user_input)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    main()
