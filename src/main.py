import argparse
import sys

from rarbg_api import RarbgApi
from models import get_torrent_type


def print_torrents(args, torrents):
    if args.torrent_type:
        type = get_torrent_type(args.torrent_type)
        i = 0
        for entry in torrents[type]:
            if (entry.is_good_quality()):
                i = i + 1
                print("{0: <3} {1}".format(i, entry))
    else:
        for k, v in torrents.items():
            print("File Type: {}".format(k.value))
            for entry in v:
                print(entry.get_title())


def main(argv):
    usage = ("python3 {FILE}").format(FILE=__file__)
    description = 'Get a list of torrents'
    parser = argparse.ArgumentParser(usage=usage, description=description)
    # parser.add_argument('--search-string', help='Query string')
    # parser.add_argument('-s', '--sort',
    #                     choices=['seeders', 'leechers', 'last'],
    #                     help='How torrents will be sorted (seeders default)',
    #                     required=False)
    # parser.add_argument('-l', '--limit',
    #                     type=int,
    #                     choices=[25, 50, 100],
    #                     default=100,
    #                     help='How many torrents will return',
    #                     required=False)
    # parser.add_argument('-c', '--category',
    #                     type=int,
    #                     help='The index of category',
    #                     required=False)
    parser.add_argument('-t', '--torrent-type',
                        choices=['RARBG', 'DEFAULT'],
                        help='The type of torrents to get',
                        required=False)
    # parser.add_argument('-v', '--verbose',
    #                     action='store_true',
    #                     help='verbose',
    #                     required=False)
    args = parser.parse_args()

    client = RarbgApi()
    torrents = client.get_torrents()

    if torrents is None:
        print("Failed to get torrents, try again later")
        exit(1)

    print_torrents(args=args, torrents=torrents)


if __name__ == '__main__':
    main(sys.argv)
