from wit import Wit
import pywapi
from flask import Flask, request
from pymessenger.bot import Bot
import requests
import os

from bayesnet import BayesNet

# Insert Wit access token here. Don't forget to train the Wit bot.
access_token = os.environ.get('WIT_TOKEN')

# Facebook App access token. Don't forge to connect app to page.
TOKEN = os.environ.get('FB_PAGE_TOKEN')

# Set up bot and flask app
bot = Bot(TOKEN)
app = Flask(__name__)

# Global variables to ensure pymessenger bot waits for wit.ai to respond.
messageToSend = 'This is default. Something is not correct'
done = False

bayes = BayesNet()
docBot = bayes.prob_symptoms

def first_entity_value(entities, entity):
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val

def send(request, response):
    """
    Sender function
    """
    # We use the fb_id as equal to session_id
    fb_id = request['session_id']
    text = response['text']
    # send message
    
    bot.send_text_message(fb_id, text)

# Calls pywapi to fetch weather info in realtime
def fetch_diagnosis(request):
    context = request['context']
    entities = request['entities']
    lst = []
    for entity in entities['name']:
        lst.append(entity['value'])

    sol_dict = docBot(lst)
 
    salt = sorted(sol_dict['_'.join(lst)].items(),
               key=lambda x: x[1], reverse=True)
    
    print(salt)
    if salt[0][1] - salt[1][1] < 0.35:
        stmt = salt[0][0]
    else:
        stmt = salt[0][0] + " or " + salt[1][0]

    context['diseases'] = stmt
    return context

def fetch_weather(session_id, context):
    location = context['loc']
    location_id = pywapi.get_loc_id_from_weather_com(location)[0][0]
    weather_com_result = pywapi.get_weather_from_weather_com(location_id)
    context['forecast'] = weather_com_result["current_conditions"]["text"]
    return context

actions = {
    'send': send,
    'fetch_diagnosis': fetch_diagnosis,
    'docbot': fetch_diagnosis
}

client = Wit(access_token, actions)

# Set up webserver and respond to messages
@app.route("/webhook", methods=['GET', 'POST'])
def hello():
    # Get request according to Facebook Requirements
    if request.method == 'GET':
        if (request.args.get("hub.verify_token") == os.environ.get('VERIFY_TOKEN')):
            return request.args.get("hub.challenge")
    # Post Method for replying to messages
    if request.method == 'POST':
        output = request.json
        event = output['entry'][0]['messaging']
        for x in event:
            if (x.get('message') and x['message'].get('text')):
                message = x['message']['text']
                recipient_id = x['sender']['id']
                client.run_actions(recipient_id, message, {})
                if done:
                    print messageToSend
                    bot.send_text_message(recipient_id, messageToSend)
            else:
                pass
        return "success"


# Default test route for server
@app.route("/")
def new():
    return "Server is Online."

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
