import requests
from datetime import datetime, time


class OpenWeatherApi:
    """

    The tool for communication with OpenWeater API.
    It allows to get forecast
    For the next 4 days for a specific location (city)

    Args:
        city (str): Name of the location to be watched
        token (str): An unique ID for API authentication
    """
    def __init__(self, city, token):
        self.city = city
        self.token = token
        self.x, self.y = self.get_x_and_y()

    def get_url(self):
        """Create url for connection to Openweathermap API.

        Returns:
            str of url for Openweathermap API.
            It will be used as base for methods which are represented below
        """
        return "https://api.openweathermap.org/data/2.5/" \
               "forecast?q={}&units=metric&appid={}" \
               .format(self.city, self.token)

    def get_json(self):
        """Gets data from API and convert it to the python dictionary.
           (finally it takes list of attibutes for a day).

        Returns:
            forecast (list): list of dictionaries with all attributes

        Example:
            [
                {'dt': 1600117200,
                 'main': {'temp': 26.2, 'feels_like': 27.87, ... },
                  ...
                 'wind': {'speed': 2.93, 'deg': 336}, ... },
                {'dt': 1600128000,
                 'main': {'temp': 24.6, 'feels_like': 26.4, ... },
                 ...
                 'wind': {'speed': 1.89, 'deg': 349}, ... },
                 ...
            ]
        """
        url_for_request = self.get_url()
        return requests.get(url_for_request).json()['list']

    def get_full_data(self):
        """Gets the forecast for 4 days
           but excludes all information which is not required
           and leaves only timestamp and speed of wind.

        Return:
            forecast (list): list of dictionaries
            with relevant information (timestamp, wind speed)

        Example:
            [
                {'timestamp': datetime.datetime(2020, 9, 15, 0, 0),
                 'wind_speed': 2.93},
                {'timestamp': datetime.datetime(2020, 9, 15, 3, 0),
                 'wind_speed': 1.89},
                ...
            ]
        """
        def get_frame(full_frame):
            """Exports only timestamp and wind speed parameters from the dictionary
               It will be used in map function
            """
            return {
                'timestamp': datetime.fromtimestamp(full_frame['dt']),
                'wind_speed': full_frame['wind']['speed'],
            }
        json_data = self.get_json()
        return list(map(get_frame, json_data))

    def get_daylight_data(self):
        """Gets only the forecast for the daytime (9:00:00 <= x <= 18:00:00)

        Returns:
            forecast (list): only relevant time periods

        Example:
            [
                {'timestamp': datetime.datetime(2020, 9, 15, 9, 0),
                 'wind_speed': 2.93},
                 ...
                {'timestamp': datetime.datetime(2020, 9, 15, 18, 0),
                 'wind_speed': 1.89},
            ]
        """
        def is_correct_time(row):
            if time(9) <= row['timestamp'].time() <= time(18):
                return True
            return False
        full_data = self.get_full_data()
        return list(filter(is_correct_time, full_data))

    def get_x_and_y(self):
        """Gets 2 list for x and y axises

        Returns:
            x (list): values for x axis (Values are converted to str)
            y (list): values for y axis (float)

        Example:
            x = ['15.09\n09:00', '15.09\n12:00', ... ]
            y = [0.7, 2.6, ... ]
        """
        data = self.get_daylight_data()
        # getting the lists from dictionary
        x_datetime = list(map(lambda x: x['timestamp'], data))
        y_not_round = list(map(lambda x: x['wind_speed'], data))
        return (
            list(map(lambda x: x.strftime('%d.%m\n%H:%M'), x_datetime)),
            list(map(lambda x: round(x, 1), y_not_round))
        )
