from table import Table
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-pp", "--proxies_path", type=str)
parser.add_argument("-cp", "--cookies_path", type=str)
parser.add_argument("-pt", "--proxy_type", choices=["http", "https", "socks5", "ssh"])
parser.add_argument("-st", "--sorting_type", choices=["ctime", "mtime", "name", "num"])

args = parser.parse_args()

if __name__ == '__main__':
    table = Table(proxies_path=args.proxies_path,
                  cookies_path=args.cookies_path,
                  proxy_type=args.proxy_type,
                  sorting_type=args.sorting_type)
    table.create()
    table.save()
