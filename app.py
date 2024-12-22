import nltk
from nltk.chat.util import Chat, reflections
import pyttsx3
import random
import datetime
import webbrowser
import wikipedia
import pyjokes

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Converts text to speech."""
    engine.say(text)
    engine.runAndWait()

# Define conversational pairs
pairs = [
    [r"hi|hello|hey", 
     ["Hello! How can I assist you today?", "Hi there! How are you doing?", "Hey! What's up?"]],
    
    [r"my name is (.*)", 
     ["Hello %1! How can I assist you?", "Nice to meet you %1. How can I help?"]],
    
    [r"(.*) your name?", 
     ["I am VBot, your virtual assistant created by Tharvesh Muhaideen A."]],
    
    [r"how are you?", 
     ["I'm just a bot, but I'm functioning perfectly. How about you?", "Doing great! How about yourself?"]],

    [r"about you | what can you do", 
     ["I can have conversations, provide jokes,fetch Wikipedia information, open websites, and tell the time.\n How can I assist you today?"]],


    [r"what time is it|current time", 
     ["The current time is " + datetime.datetime.now().strftime("%H:%M:%S")]],
    
    [r"tell me a joke", 
     [pyjokes.get_joke(), "Here's a funny one: " + pyjokes.get_joke()]],
    
    [r"search for (.*)", 
     ["Searching for %1 on Wikipedia.", "Let me fetch information about %1 for you."]],
    
    [r"open (.*) website", 
     ["Opening %1 website."]],
    
    [r"quit|bye|exit", 
     ["Goodbye! Have a wonderful day.", "Bye! Feel free to chat anytime."]],
    
    [r"(.*)", 
     ["I'm not sure I understand that. Could you rephrase?", "Interesting! Can you explain more about that?", "Let's explore something else. What would you like to discuss?"]]
]

# Chatbot class with added functionality
class VBotChat(Chat):
    def respond(self, statement):
        """Generates a response and handles dynamic actions."""
        response = super().respond(statement)
        speak(response)
        
        # Open website
        if "Opening" in response:
            site_name = statement.split()[-1]
            url = f"https://{site_name}.com"
            webbrowser.open(url)
            return f"Opening {site_name} website."
        
        # Search Wikipedia
        elif "Searching for" in response:
            query = statement.split("search for")[-1].strip()
            try:
                summary = wikipedia.summary(query, sentences=2)
                speak(summary)
                return summary
            except Exception as e:
                error_message = f"Couldn't fetch information: {str(e)}"
                speak(error_message)
                return error_message
        
        return response

# Initialize chatbot with pairs and reflections
chatbot = VBotChat(pairs, reflections)

def start_chat():
    """Starts the chatbot conversation."""
    intro = (
        "Hello! I am VBot, your virtual assistant. I can have conversations, provide jokes, "
        "fetch Wikipedia information, open websites, and tell the time.\n How can I assist you today?"
    )
    print(intro)
    speak(intro)
    chatbot.converse()

if __name__ == "__main__":
    start_chat()
