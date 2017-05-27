# Source: https://www.codementor.io/garethdwyer
# /building-a-telegram-bot-using-python-part-1-goi5fncay

import json, requests, time, urllib

with open('token.txt', 'r') as f:
    bot_token = f.readline().strip()

base_url = "https://api.telegram.org/bot{}/".format(bot_token)

# Does a GET request on a full-length URL and returns a UTF8-decoded response
# Decoding: Bytes to characters
# Encoding: Characters to bytes
# Unicode Transformation Format 8 (i.e. uses 8-bit blocks to represent a char)
# UTF-8 is a compromise character encoding that can be as compact as ASCII
def http_get(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

# Does a GET request on a full-length URL and returns a JSON-deserialized Python object
# Deserialization: Extracting a data structure from a series of bytes (e.g. string)
# Serialization: Translating a data structure into a format (e.g. string) for storage
def get_json_from_url(url):
    content = http_get(url)
    js = json.loads(content)
    return js

# Returns a Python object (JSON format) containing updates (e.g. messages received)
# Bot will initiate a new check every minute, or whenever a new message is received
# Updates of ID strictly smaller than a specified offset are omitted from the response
# Sample response: {"ok":true,"result":[
# {"update_id":NUMBER,"message":{"message_id":1,"from":{"id":NUMBER,
# "first_name":"UTF8-encoded","language_code":"en-GB"},"chat":{"id":NUMBER,
# "first_name":"UTF8-encoded","type":"private"},"date":EPOCH,"text":"TEXT"}},
# {"update_id":NUMBER,"message":{"message_id":3,"from":{"id":NUMBER,
# "first_name":"UTF8-encoded","language_code":"en-GB"},"chat":{"id":NUMBER,
# "first_name":"UTF8-encoded","type":"private"},"date":EPOCH,"text":"TEXT"}}]}
# update_id identifies updates from the senders (non-bots)
# message_id is the position of the message in the entire archive of that chat
def get_updates(offset = None):
    url = base_url + "getUpdates?timeout=60"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

# Gets the latest update ID
# Use case: We can then request for the latest X updates by calculating and specifying
# the offset in get_updates
def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

# Gets latest chat ID and the corresponding text
# Chat ID identifies the sender
def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

# (Bot) sends a message to a specified chat ID (i.e. a prompt or a reply)
# quote_plus replaces special characters in string using the %xx escape
# Letters, digits, and the characters '_.-' are never quoted
# quote_plus also replaces spaces by plus signs for quoting HTML form values
# when building up a query string to go into a URL
def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = base_url + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    http_get(url)

# Reply the sender of each update with the corresponding received message (echo)
def echo_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            send_message(text, chat)
        except Exception as e:
            print(e)

def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(1)

if __name__ == '__main__':
    main()
