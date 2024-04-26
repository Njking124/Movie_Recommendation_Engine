import os
import torch
from dotenv import load_dotenv
import logging
import spacy
from profanity_filter import ProfanityFilter
import json
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import openai
import onMovie
import image
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext


load_dotenv()
# Telegram Bot Token
TOKEN = os.getenv('Telegram')

# Telegram API setup
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Your existing code

openai.organization = os.getenv('organization')
openai.api_key = os.getenv('OPENAI_API_KEY')

model_name = 'gpt2'
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

user_data = {}
questions = [
"Genre Preferences",

"Think hard about the kind of movie you want to watch \N{thinking face}. Are there any movies that match the vibe?",

"What’s the audience for tonight? \N{movie camera} Choose a rating from the following: G, PG, PG-13, R.",

"How far are we going back? \N{eyes} Pick a decade.",

"How much time do we have on our hands? \N{watch} Do you want to watch a short, medium, or long movie?",

"Feeling starstruck? \N{glowing star} Any actors or directors you knead to see?",

"Anything else we should consider? The floor is yours. \N{man dancing} Think emotions, settings, tropes, plots, etc.",

"I'll now begin the movie baking process. \N{face without mouth} Stay put, I’m off to bake the perfect movie for you. \N{clapper board} Are you excited?",

"The movie is fresh out of the oven! \N{bread} Here is my personalized recommendation. No need to thank me, it’s the yeast I can do. \N{winking face}",

"I hope you love it as much as I loved talking to you. Here are my individualised, tailored recommendations.",

"This is it for me. Take care, ok?"
]

question_index = 0
question_names = ["genres", "similar_movies", "maturity", "decade", "length", "actor-director", "textbox"]
# url, text
nlp = spacy.load("en_core_web_sm")
profanity_filter = ProfanityFilter(nlps={'en': nlp})
nlp.add_pipe(profanity_filter.spacy_component, last=True)

def getMovie(user_data):
    title = onMovie.take_input(user_data)
    url = image.image_url(title)
    print("getmov")
    return url, title

def start(update, context):
    update.message.reply_text("Hi! I'm your movie recommendation bot. Let's get started!")
    update.message.reply_text("When listing your preferences please enter a comma-separated list. If you don’t have a preference, enter no. ❌")
    update.message.reply_text("Let’s start simple. Do you have any genre preferences? 🎞")
    update.message.reply_text("If so, choose from the following: Action, Adventure, Biography, Comedy, Crime, Drama, Family, Fantasy, History, Horror, Musical, Mystery, Romance, Sci-Fi, Sport, Thriller, War, Western")
    context.user_data['question_index'] = 0
    context.user_data['user_data'] = {}

def process_input(update, context):
    user_input = update.message.text
    question_index = context.user_data['question_index']
    user_data = context.user_data['user_data']
    
    if question_index <= len(question_names) - 1:
        user_data[question_names[question_index]] = user_input
    
    print(user_data)

    result_list = user_input.split(',')

    prompt = "I love " + result_list[0] + " movies"
    if result_list[0] in ["G", "PG", "PG-13"]:
        prompt = "I love " + result_list[0] + " rated movies for kids"
    if result_list[0] == "romance":
        prompt = "I love sweet and kind movies"
    if result_list[0] == "long":
        prompt = "I prefer three hour movies over 1 hour movies"

    completion = "?"
    if question_index <= 5:
        input_ids = tokenizer.encode(prompt, return_tensors="pt", add_special_tokens=True)
        attention_mask = torch.ones(input_ids.shape, dtype=torch.long)
        output = model.generate(input_ids, attention_mask=attention_mask, max_length=100, num_return_sequences=1)[0]
        completion = tokenizer.decode(output, skip_special_tokens=True)

        pos = 0
        for i in range(len(completion)):
            if completion[i].isupper():
                pos = i
                break
        completion = completion[pos:]
    else:
        completion = "noneC"
    
    if result_list[0].lower() == "no":
        completion = "It's okay! I'm indecisive too sometimes \N{relieved face}"
    
    if len(user_data) == len(question_names) and question_index == 7:
        
        movieURL, movieText = getMovie(user_data)
    else:
        movieURL = "noneU"
        movieText = "noneT"
    
    question_index += 1
    
    # Sending the reply back to the user
    if movieURL!="noneU" and movieText!="noneT":
        update.message.reply_text(f"{questions[question_index]}")
        update.message.reply_text(f"{completion}")
        update.message.reply_text(f"{movieURL}\n{movieText}")
        
    else:
        update.message.reply_text(f"{questions[question_index]}")
        update.message.reply_text(f"{completion}")
        
    
    
    # Updating user data and question index
    context.user_data['question_index'] = question_index
    context.user_data['user_data'] = user_data


def unknown(update, context):
    update.message.reply_text("Sorry, I don't understand that command.")

# Adding handlers to the dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, process_input))
dispatcher.add_handler(MessageHandler(Filters.command, unknown))

# Start the bot
updater.start_polling()
updater.idle()
