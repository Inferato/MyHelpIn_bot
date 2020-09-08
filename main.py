import requests
import datetime
from wethr import getweather
token = "1037730614:AAG4BR2gc9b157zZhbxVUYhtmg55oaAindU"


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def deletewebhook(self):
        method = 'deleteWebhook'
        resp = requests.get(self.api_url+method)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
            return last_update


greet_bot = BotHandler(token)
greetings = ('здравствуй', 'привет', 'ку', 'здорово')
now = datetime.datetime.now()


def main():
    new_offset = None
    today = now.day
    hour = now.hour

    while True:
        greet_bot.deletewebhook()
        greet_bot.get_updates(new_offset)

        last_update = greet_bot.get_last_update()
        if last_update:
            last_update_id = last_update['update_id']
            last_chat_text = last_update['message']['text']
            last_chat_id = last_update['message']['chat']['id']
            last_chat_name = last_update['message']['chat']['first_name']

            if last_chat_text.lower() in greetings and today == now.day and 6 <= hour < 12:
                greet_bot.send_message(last_chat_id, 'Доброе утро, {}'.format(last_chat_name))
                # today += 1

            elif last_chat_text.lower() in greetings and today == now.day and 12 <= hour < 17:
                greet_bot.send_message(last_chat_id, 'Добрый день, {}'.format(last_chat_name))
                # today += 1

            elif last_chat_text.lower() in greetings and today == now.day and 17 <= hour < 23:
                greet_bot.send_message(last_chat_id, 'Добрый вечер, {}'.format(last_chat_name))
                # today += 1

            elif last_chat_text.lower() == "погода":
                resp = getweather()
                descpiption = resp['weather'][0]['description']
                temp = resp['main']['temp']
                feels_like = resp['main']['feels_like']
                temp_min = resp['main']['temp_min']
                temp_max = resp['main']['temp_max']
                name = resp['name']
                weather = "Выбранный город:  {}".format(name) + \
                          "\n " + descpiption + "\n температура: {}С".format(temp) + \
                    "\n чувствуется как: {}C".format(feels_like) + \
                    "\n минимальная температура: {}C".format(temp_min) + \
                    "\n максимальная температура: {}C".format(temp_max)
                greet_bot.send_message(last_chat_id, 'Прогноз погоды на сейчас: \n {}'.format(weather))

            new_offset = last_update_id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
        main()