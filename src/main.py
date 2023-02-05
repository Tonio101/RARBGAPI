import argparse
import sys

from rarbg_api import RarbgApi
from prettytable import PrettyTable
from models import get_torrent_type


from logger import Logger
log = Logger.getInstance().getLogger()


def get_torrent_dict(args, torrents) -> dict:
    torrent_dict = dict()

    i = 0
    if args.torrent_type:
        type = get_torrent_type(args.torrent_type)
        for entry in torrents[type]:
            if (entry.is_good_quality()):
                i = i + 1
                log.debug("{0: <3} {1}".format(i, entry))
                torrent_dict[i] = entry
    else:
        for k, v in torrents.items():
            log.debug("File Type: {}".format(k.value))
            for entry in v:
                i = i + 1
                log.debug("{0: <3} {1}".format(i, entry))
                torrent_dict[i] = entry

    return torrent_dict


def print_table(torrent_dict: dict) -> None:
    table = PrettyTable(["No.", "Title", "Seeders",
                        "Leechers", "Size (GB)", "Date"])
    for i, entry in torrent_dict.items():
        table.add_row([
            i,
            entry.get_title(),
            entry.get_seeders(),
            entry.get_leechers(),
            entry.get_size_gb(),
            entry.get_date()
        ])

    table._align["No."] = "l"
    table._align["Title"] = "l"

    print(table)


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

    log.info('This is a test meesage')

    client = RarbgApi()
    torrents = client.get_torrents()

    if torrents is None:
        log.info("Failed to get torrents, try again later")
        exit(1)

    torrent_dict = get_torrent_dict(args=args, torrents=torrents)
    print_table(torrent_dict)
    torrent_input = input("Select a number to get torrent link or cancel[c]: ")
    if 'c' == torrent_input:
        exit(0)

    if not isinstance(torrent_input, int):
        log.error("Invalid input, expected an integer value")
        exit(1)

    selection = int(torrent_input)
    if selection in torrent_dict:
        print(torrent_dict[int(selection)].get_download())


if __name__ == '__main__':
    main(sys.argv)
