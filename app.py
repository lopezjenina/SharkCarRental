from flask import Flask, request, jsonify, render_template
import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model

lemmatizer = WordNetLemmatizer()

app = Flask(__name__)

# Load chatbot model, words, and classes
model = load_model('my_chatbot.h5')
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))

with open('intents.json', 'r') as file:
    intents = json.load(file)

# Chatbot functions (clean_up_sentence, bag_of_words, predict_class) - Same as your chatbot.py
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]  # Corrected lemmatization
    return sentence_words

# Converting sentence function
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1  # Corrected setting bag values
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)  # Corrected sorting

    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

print("Hi! I'm online. Let's chat!")

# API endpoint for receiving and responding to messages
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    message = request.json['message']
    ints = predict_class(message)
    response = get_response(ints, intents)  # Pass intents as the second argument
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
