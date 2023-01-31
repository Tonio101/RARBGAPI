import requests
import platform
import time

from models import RarbgFile, TorrentType

REQUESTS_RETRY = 10
# Docs: https://torrentapi.org/apidocs_v2.txt
TORRENT_API_HOST = "https://torrentapi.org/pubapi_v2.php"


class RarbgApi(object):

    def __init__(self, api=TORRENT_API_HOST) -> None:
        self.api = api
        self.token = None
        self.app_id = self.__get_app_name()
        self.last_request_time = 0
        self.token_expired = True

    def __get_app_name(self) -> str:
        return ("{}_{}_{}_{}").format(
            platform.system(),
            platform.node(),
            platform.machine(),
            platform.python_version()
        )

    def __get_token(self):
        params = {
            'app_id': self.app_id,
            'get_token': 'get_token'
        }
        print(self.app_id)
        response = requests.get(url=self.api, params=params)

        if response.status_code == 200:
            data = response.json()
            print("Token {}".format(
                data
            ))
            self.token = data['token']
            self.token_expired = False
        else:
            print("Request failed with status code:", response.status_code)

    def __get_torrents(self, sort='seeders',
                       category='movies', limit=100) -> dict:
        params = {
            'app_id': self.app_id,
            'mode': 'list',
            'format': 'json_extended',
            'category': category,
            'limit': limit,
            'sort': sort,
            'token': self.token
        }

        rarbg_file_dict = dict()
        for t in TorrentType:
            rarbg_file_dict[t] = []

        response = requests.get(url=self.api, params=params)
        if response.status_code == 200:
            data = response.json()
            torrent_files = data['torrent_results']
            print("Size of torrent list: {}".format(len(torrent_files)))
            for torrent_file in torrent_files:
                rarbg_file = RarbgFile(torrent_file)
                rarbg_file_dict[rarbg_file.get_type()].append(rarbg_file)
        elif response.status_code == 401:
            print("Token expired")
            self.token_expired = True
            return None
        else:
            print("Torrent request failed with code:", response.status_code)
            return None

        return rarbg_file_dict

    def get_torrents(self):
        result = None

        for i in range(REQUESTS_RETRY):
            print("Making request attempt {}".format(i))
            result = self.get_torrents_rate_limited()
            if result:
                break

        return result

    def get_torrents_rate_limited(self, sort='seeders',
                                  category='movies', limit=100) -> dict:
        current_time = time.time()
        if current_time - self.last_request_time < 0.5:
            time.sleep(0.5 - (current_time - self.last_request_time))
        self.last_request_time = time.time()

        if self.token_expired:
            self.__get_token()
        return self.__get_torrents()
