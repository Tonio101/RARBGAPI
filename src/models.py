import re

from enum import Enum

from logger import Logger
log = Logger.getInstance().getLogger()


class TorrentType(Enum):
    DEFAULT = "DEFAULT"
    RARBG_TYPE = "RARBG"


def get_torrent_type(name: str) -> TorrentType:
    for t in TorrentType:
        if t.value in name:
            return t
    return TorrentType.DEFAULT


class RarbgFile(object):

    def __init__(self, raw_dict) -> None:
        self.is_1080p = False
        self.is_extended = 'title' in raw_dict
        self.raw_title = raw_dict['title'] or raw_dict['filename']
        self.type = get_torrent_type(name=self.raw_title)
        self.title = self.get_santized_title()
        self.category = raw_dict['category']
        self.download = raw_dict['download']
        self.seeders = raw_dict['seeders']
        self.leechers = raw_dict['leechers']
        self.size = raw_dict['size']
        self.pubdate = raw_dict['pubdate']
        self.episode_info = raw_dict['episode_info']
        self.ranked = raw_dict['ranked']
        self.info_page = raw_dict['info_page']

    def get_title(self) -> str:
        return self.title

    def get_type(self) -> TorrentType:
        return self.type

    def is_good_quality(self) -> bool:
        return self.is_1080p

    def bytes_to_gb(self, bytes) -> float:
        return round((bytes / (1024**3)), 2)

    def get_seeders(self) -> int:
        return self.seeders

    def get_leechers(self) -> int:
        return self.leechers

    def get_size_gb(self) -> float:
        return self.bytes_to_gb(self.size)

    def get_date(self) -> str:
        return self.pubdate

    def get_download(self) -> str:
        return self.download

    def get_santized_title(self) -> str:
        if self.type == TorrentType.RARBG_TYPE:
            match = re.search(r"(.*)\.1080p.*RARBG$", self.raw_title)
            if match:
                self.is_1080p = True
                return match.group(1)
        # elif self.type == TorrentType.DEFAULT:

        return self.raw_title

    def __str__(self) -> str:
        return ("{0} {1: <50} Seeders[{2}] Leechers[{3}] Size[{4}]").format(
            self.pubdate,
            self.title,
            self.seeders,
            self.leechers,
            self.bytes_to_gb(self.size)
        )
