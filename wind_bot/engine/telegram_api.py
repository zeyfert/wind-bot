import requests


class TelegramApi:
    """

    Telegram dispatcher which allows:
        - Check a new message in a specific chat
        - Send respond as diagram
          (Diagram is build based on data from OpenWeather API)

    Args:
        token (str): An unique ID for bot authentication.
        telegram_url (str): Telegram API url based on token

    Official documentation:
        https://core.telegram.org/bots/api

    In the next version:
        - Should be added exception for get_telegram_url

    """
    def __init__(self, token):
        self.token = token
        self.telegram_url = self.get_telegram_url()

    def get_telegram_url(self):
        """Create url for connection to Telegram API.

        Returns:
            str of url for Telegram API.
            It will be used as base for methods
            which are represented below
        """
        return 'https://api.telegram.org/bot{}/'.format(self.token)

    def get_updates(self, offset=None, timeout=30):
        """Gets all non-confirmed updates (messages)
           based on offset value

        Args:
            offset (int): The value helps to identify
            if value has been already read by the bot
            timeout (int): The value is used for long polling
            in order to reduce the overload on the servers

        Official documentation (getUpdates method):
            https://core.telegram.org/bots/api#getupdates

        Returns:
            Result of the get-request.
            May equals:
            1) Empty list. It means that no updates were found
            2) List of dictionaries with attributes of messages
        """
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        return requests.get(self.telegram_url + method, params) \
            .json()['result']

    def get_chat_attributes(self, new_messages):
        """Gets the last message after using get_updates() method.

        Args:
            new_messages (list): the list of messages
            (But actually it may be one message in the list)

        Returns:
            Dictionary with all attributes
            which are required for the next step
            (recognize message and respond)

        """
        return {
            'last_update_id': new_messages[-1]['update_id'],
            'chat_id': new_messages[-1]['message']['from']['id'],
            'message': new_messages[-1]['message']['text']
        }

    def send_photo(self, chat_id, photo):
        """Sends photo to the specific chat

        Args:
            chat_id (int): ID of the chat which should get the message
            photo (buffered bytes object): photo (diagram) to upload

        Returns:
            Response code (For confirmation that everything is correct.
            It will be deleted in the next version).
            In the next version will be added an Exception
            (in the case if respond != 200)
        """
        method = 'sendPhoto'
        params = {'chat_id': chat_id}
        files = {'photo': photo}
        return requests.post(
            self.telegram_url + method,
            data=params,
            files=files
        )
