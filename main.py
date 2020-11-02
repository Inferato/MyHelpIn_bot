import requests
import datetime
from wethr import getweather
from googletrans import Translator

# it`s a pet proj for study
token = "1037730614:AAG4BR2gc9b157zZhbxVUYhtmg55oaAindU"
translator = Translator()


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

            if last_chat_text.lower() == "погода":
                greet_bot.send_message(last_chat_id, 'Укажите Ваш город: ')
                new_offset = last_update_id + 1
                greet_bot.deletewebhook()
                greet_bot.get_updates(new_offset)
                last_update = greet_bot.get_last_update()
                if last_update:
                    last_chat_text = last_update['message']['text']
                    city_translate = str(translator.translate(last_chat_text.capitalize(), 'uk', 'ru').text)
                    city = str(translator.translate(city_translate, 'en', 'uk').text)
                    try:
                        resp = getweather(city)
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
                    except KeyError as e:
                        greet_bot.send_message(last_chat_id, 'Прогноз погоды на сейчас: \n{}'.format(str(translator.translate(resp['message'], 'ru', 'en').text)))

            new_offset = last_update_id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
