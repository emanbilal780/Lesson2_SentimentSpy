# import nltk

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')

import colorama
from colorama import Fore, Style
from textblob import TextBlob

colorama.init()

print(f"{Fore.CYAN} 🐍 Welcome to Sentiment Spy! 🐍{Style.RESET_ALL}")

user_name = input(f"{Fore.MAGENTA}Please enter your name: {Style.RESET_ALL}").strip()
if not user_name:
    user_name = "Mystery Agent"  # Fallback if user doesn't provide a name

# Store conversation as a list of tuples: (text, polarity, sentiment_type)("Hi","positive","Neutral")
conversation_history = []

print(f"\n{Fore.CYAN}Hello, Agent {user_name}!")
print(f"Type a Sentence and I will analyze your sentences with TextBlob and show you the sentiment. ")
print(f"Type {Fore.YELLOW}reset{Fore.CYAN}, {Fore.YELLOW}history{Fore.CYAN}, "
    f"or {Fore.YELLOW}exit{Fore.CYAN} to quit.{Style.RESET_ALL}\n")

def fact_or_opinion(subjectivity):
    if subjectivity > 0.5:
        return "Opinion 💭"
    return "Fact 📘"

def mood_bar(polarity, width=20):
    """Return a bar like [#########|          ] showing -1 to +1."""
    pos = int((polarity + 1) / 2 * width)
    return "[" + "█" * pos + "-" * (width - pos) + "]"


while True:
    user_input = input(f"{Fore.GREEN}>> {Style.RESET_ALL}").strip()

    if not user_input:
        print(f"{Fore.RED}Please enter some text or a valid command.{Style.RESET_ALL}")
        continue

    # Check for commands
    if user_input.lower() == "exit":
        print(f"\n{Fore.BLUE} Exiting Sentiment Spy. Farewell, Agent {user_name}! 😊{Style.RESET_ALL}")
        break

    elif user_input.lower() == "reset":
        conversation_history.clear()
        print(f"{Fore.CYAN} All conversation history cleared!{Style.RESET_ALL}")
        continue

    elif user_input.lower() == "help":
        print(f"{Fore.CYAN}Commands: history, stats, reset, help, exit{Style.RESET_ALL}")
        continue

    elif user_input.lower() == "stats":
        if not conversation_history:
            print(f"{Fore.YELLOW}Type some sentences first!{Style.RESET_ALL}")
        else:
            avg = sum(p for _, p, _ in conversation_history) / len(conversation_history)
            happiest = max(conversation_history, key=lambda x: x[1])
            saddest = min(conversation_history, key=lambda x: x[1])
            print(f"{Fore.CYAN}Sentences analyzed: {len(conversation_history)}")
            print(f"Average mood: {avg:.2f} {mood_bar(avg)}")
            print(f"Happiest: {happiest[0]} ({happiest[1]:.2f})")
            print(f"Saddest: {saddest[0]} ({saddest[1]:.2f}){Style.RESET_ALL}")
        continue

    elif user_input.lower() == "history":
        if not conversation_history:
            print(f"{Fore.YELLOW}No conversation history yet.{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN} Conversation History:{Style.RESET_ALL}")
            for idx, (text, polarity, sentiment_type) in enumerate(conversation_history, start=1):
                # Choose color & emoji based on sentiment
                if sentiment_type == "Positive":
                    color = Fore.GREEN
                    emoji = "😊"
                elif sentiment_type == "Negative":
                    color = Fore.RED
                    emoji = "😞"
                else:
                    color = Fore.YELLOW
                    emoji = "😭"

                print(f"{idx}. {color}{emoji} {text} "
                    f"Polarity: {polarity:.2f}, {sentiment_type}{Style.RESET_ALL}")
        continue

    # Analyze sentiment
    blob = TextBlob(user_input)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    if polarity > 0.25:
        sentiment_type, color, emoji = "Positive", Fore.GREEN, "😊"
    elif polarity < -0.25:
        sentiment_type, color, emoji = "Negative", Fore.RED, "😞"
    else:
        sentiment_type, color, emoji = "Neutral", Fore.YELLOW, "😐"

    conversation_history.append((user_input, polarity, sentiment_type))

    print(f"{color}{emoji} {sentiment_type} sentiment detected! Polarity: {polarity:.2f}")
    print(f"{color}Mood meter: {mood_bar(polarity)}")
    print(f"{color}This sounds like: {fact_or_opinion(subjectivity)} "
          f"(subjectivity {subjectivity:.2f}){Style.RESET_ALL}")