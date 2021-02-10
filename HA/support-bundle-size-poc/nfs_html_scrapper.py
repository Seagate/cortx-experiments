from lxml import html
from argparse import ArgumentParser
import requests

def parse_args():
    parser = ArgumentParser(description="Srap FTP webpage for support bundles")
    parser.add_argument("--filename", type=str, default="SUPPORT_BUNDLE", help="Files to search")
    parser.add_argument("--maxsize", type=int, default=1_000_000_000, help="Maximum size in bytes to search from")
    # Nodes to setup cluster can be entered via file or via parameters
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("url", type=str, nargs="?", help="URL to index.html page")
    group.add_argument("--testfile", required=False, type=str, help="Index html file for debug ONLY")
    return parser.parse_args()

def read_from_file(filename):
    with open(filename) as f:
        return f.read()

def read_from_url(url):
    return requests.get(url).content

def parse_index_html(tree, url, options):
    subdir_list = []
    for link in tree.findall('.//a'):
        filename = link.get('href')
        rest_line = link.tail

        # Skip link to upper directory
        if link.text_content().startswith('..'):
            continue
        #print(f"{filename}{rest_line}")

        # Skip directories for now - they will be processed in the end
        if filename.endswith('/'):
            #print(f"{filename} will be processed later")
            subdir_list.append(filename)
            continue

        # Get the size of the file, cause we expect only files left
        filesize = int(rest_line.split(' ')[-1].rstrip('\n'))

        #print(f"{url}/{filename};{filesize}")
        if filesize > options['maxsize'] and filename.startswith(options['pattern']):
            print(f"RESULT;{url}{filename};{filesize}")

    for d in subdir_list:
        traverse_ftp_tree(url + d, options)

def traverse_ftp_tree(url, options):
    #print(f"Looking into {url}")
    page = read_from_url(url)
    tree = html.fromstring(page)
    parse_index_html(tree, url, options)


def main(args):
    #import pdb
    #pdb.set_trace()
    if args.testfile:
        page = read_from_file(args.testfile)
        tree = html.fromstring(page)
        return

    traverse_ftp_tree(args.url, {'pattern':args.filename, 'maxsize':args.maxsize})

if __name__ == "__main__":
    args = parse_args()
    main(args)
