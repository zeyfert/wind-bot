from prompt import string
from wind_bot.engine.telegram_api import TelegramApi
from wind_bot.engine.openweather_api import OpenWeatherApi
from wind_bot.engine.diagram import create_graph


def main():
    """

    Method connects to Telegram API and checks the new messages in a chat
    And sends the diagram as respond in the case
    If message equals 'w' or 'wind'

    In the next version:
        - Should be added the checkong function for API's

    """
    telegram_token = string('Please enter a token for Telegram API ')
    telegram_bot = TelegramApi(telegram_token)
    open_weather_token = string('Please enter a token for OpenWeather API ')
    city = string('Please enter a city ')
    openweather_parcer = OpenWeatherApi(city, open_weather_token)
    new_offset = None
    while True:
        new_messages = telegram_bot.get_updates(new_offset)
        if new_messages == []:
            pass
        else:
            chat_attributes = telegram_bot.get_chat_attributes(new_messages)
            last_update_id, chat_id, message = chat_attributes.values()
            if message in ['w', 'wind']:
                x, y = openweather_parcer.get_x_and_y()
                graph = create_graph(x, y)
                response = telegram_bot.send_photo(chat_id, graph)
                print(response)
            else:
                print("""I couldn't recognize the message.
                       Please type 'w' or 'wind'""")
            new_offset = last_update_id + 1
            print(new_messages)


if __name__ == '__main__':
    main()
