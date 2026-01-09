# from chatterbot import ChatBot
# from chatterbot.trainers import ChatterBotCorpusTrainer
# 
# chatbot = ChatBot('Ron Obvious')
# 
# # Create a new trainer for the chatbot
# trainer = ChatterBotCorpusTrainer(chatbot)
# 
# # Train the chatbot based on the english corpus
# trainer.train("chatterbot.corpus.english")
# 
# # Get a response to an input statement
# chatbot.get_response("Hello, how are you today?")

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

import re
michael = ChatBot("Michael")

trainer = ListTrainer(michael)
trainer_corpus = ChatterBotCorpusTrainer(michael)
# 

# while True:
#     with open('output3.txt', 'r', encoding='utf-8') as file:
#     # Read the lines from the file
#         lines = file.readlines()
# 
#     # Split the lines into a list of conversations
#     # Assuming each pair of lines forms a single conversation
#         conversations = [lines[i:i + 2] for i in range(0, len(lines), 2)]
# 
#     # Train the bot with each conversation
#     for conversation in conversations:
#         trainer.train(conversation)
#     trainer_corpus.train(
#     "chatterbot.corpus.english"
#     )
# 
# 
#     trainer.train([
#         "Hi",
#         "I'm Michael",
#         "Maybe I can have an easy life",
#         "Mechanical is cool has an enlarged learn",
#         ])
#     trainer.train([
#         "What do you need help with today?",
#         "I can help with fetching files, getting articles and tutorials, etc",
#         ])
#     True
exit_conditions = (":q","quit","exit")
while True:
    query = input("You: ")
    if query in exit_conditions:
        break
    else:
        print(f"Michael: {michael.get_response(query)}")