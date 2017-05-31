# Sources:
# Building a Chatbot using Telegram and Python (Part 1) by Gareth Dwyer

import json, requests, time, urllib
from db_helper import DBHelper

db = DBHelper()

with open('token.txt', 'r') as f:
    bot_token = f.readline().strip()

base_url = 'https://api.telegram.org/bot{}'.format(bot_token)

replies = {}
with open('replies.txt', 'r') as m:
    num_lines, command = m.readline().strip().split(' ')
    num_lines = int(num_lines)
    while num_lines:
        replies[command] = []
        for i in range(num_lines):
            replies[command].append(m.readline().strip())
        num_lines, command = m.readline().strip().split(' ')
        num_lines = int(num_lines)

reporters = {}

timeout_main = 300
timeout_ask = 180

def get_json_from_url(url):
    response = requests.get(url)
    decoded_content = response.content.decode('utf-8')
    return json.loads(decoded_content)

def get_updates(timeout, offset = None):
    url = '{}/getUpdates?timeout={}'.format(base_url, timeout)
    if offset:
        url += '&offset={}'.format(offset)
    return get_json_from_url(url)

def get_latest_update_id(updates):
    update_ids = []
    for update in updates['result']:
        update_ids.append(int(update['update_id']))
    return max(update_ids)

def get_latest_chat_id_and_text(updates):
    text = updates['result'][-1]['message']['text']
    chat_id = updates['result'][-1]['message']['chat']['id']
    return (text, chat_id)

def send_message(text, chat_id, reply_markup = None):
    text = urllib.parse.quote_plus(text)
    url = '{}/sendMessage?text={}&chat_id={}&parse_mode=Markdown'.format(base_url, text, chat_id)
    if reply_markup:
        url += '&reply_markup={}'.format(reply_markup)
    requests.get(url)

def handle_updates(updates, latest_update_id):
    for update in updates['result']:
        try:
            text = update['message']['text']
            chat = update['message']['chat']['id']
            sender = update['message']['from']['id']

            if sender in reporters:
                reporters[sender].append(text)
                reporters[sender][0] += 1
                if reporters[sender][0] >= len(replies['questions']):
                    send_message(replies['thanks'][0], chat)
                    db.insert(reporters[sender][1:])
                    reporters.pop(sender)
                    continue
                send_message(replies['questions'][reporters[sender][0]], chat)
            elif text == '/help':
                send_message(replies[text][0], chat)
            elif text == '/start':
                send_message('\n'.join(replies[text]), chat)
            elif text == '/report':
                send_message(replies[text][0], chat)
                reporters[sender] = [0]
                send_message(replies['questions'][0], chat)
            elif text == '/view':
                send_message(replies[text][0] + db.select_recent_pretty(), chat)
            else:
                send_message(replies['dk'][0], chat)
        except KeyError:
            pass

def main():
    db.create_table()
    latest_update_id = None
    while True:
        updates = get_updates(timeout_main, latest_update_id)
        if updates['result']:
            latest_update_id = get_latest_update_id(updates) + 1
            handle_updates(updates, latest_update_id)
        time.sleep(1)

if __name__ == '__main__':
    main()
