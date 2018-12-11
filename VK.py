import requests
from urllib.parse import urljoin
from pprint import pprint

APP_ID = 6776462
TOKEN = 'f159fdd8f159fdd8f159fdd8ccf13e9b56ff159f159fdd8ad5229b3ef78a9ccbbed4689'
AUTH_URL = 'https://oauth.vk.com/authorize'
URL_API = 'https://api.vk.com/method/'
URL_START = str('https://vk.com/id')

SOURCE_USER = 1895319
TARGET_USER = 83175

class ProfileIsPrivateException(RuntimeError):
    """ Thrown when profile is private """


def find_all(friend_one, friend_two):
    return list(set(friend_one) & set(friend_two))

class User():

    def __init__(self, user_id):
        self.user_id = user_id

    def _normalize(self, user_list):
        """
        input: List of either integers or dictionaries containing among others integers.
        output: A list of integers representing identifiers.
        """
        assert isinstance(user_list, list), 'Struct must be a list'

        if isinstance(user_list[0], int):
            return user_list
        if isinstance(user_list[0], dict):
            ids = []
            for user in user_list:
                ids.append(user['id'])
            return ids
        raise TypeError('Unknown data structure')

    def mutual_friends(self, user_id=None):
        params = {
            'access_token': TOKEN,
            'source_uid': SOURCE_USER,
            'v': '5.92',
            'user_id': user_id if user_id else self.user_id,
            'fields': 'first_name',

        }
        resp = requests.get(URL_API + 'friends.get', params=params)
        result = resp.json()
        if 'error' in result:
            if result.get('error', {}).get('error_code') == 30:
                raise ProfileIsPrivateException(
                    result.get('error', {}).get('error_msg'))
        return result['response']['items']

    def __and__(self, other):
            user_1 = self.mutual_friends()
            user_2 = other.mutual_friends()
            mutual_friends = find_all(
                self._normalize(user_1), self._normalize(user_2))
            return mutual_friends

    def __str__(self):
        return urljoin(URL_START, str(self.user_id))

def main():
    user_1 = User(SOURCE_USER)
    target_id = User(TARGET_USER)
    pprint(user_1 & target_id)
    print(target_id)

if __name__ == '__main__':
    main()
