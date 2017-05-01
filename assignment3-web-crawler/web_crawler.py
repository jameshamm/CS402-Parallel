import os
import requests

from bs4 import BeautifulSoup
from urllib import parse

EXTENSION = "html"


def save_page_to_file(response, foldername):
    xs = parse.urlsplit(response.url)
    filename = xs.netloc + xs.path
    if filename.endswith('/'):
        filename = filename[:-1]
    filename += '.' + EXTENSION

    file = os.path.join(foldername, filename)
    folder, filename = file.rsplit('/', 1)
    try:
        os.makedirs(folder)
    except FileExistsError:
        pass

    if os.path.exists(file):
        print("file already exists, skipping", file)
    else:
        with open(file, 'wb+') as f:
            f.write(response.content)
        print("Saved:", file)


def req(url):
    # Get the page
    response = requests.get(url)

    # Find all link in the page
    soup = BeautifulSoup(response.text, 'lxml')
    links = [link.get('href') for link in soup.find_all('a')]

    # Make them valid links
    links = [parse.urljoin(response.url, link) for link in links]
    return response, links

def get_url(url, fname=None):
    response, links_on_page = req(url)

    # Make a folder
    if fname is None:
        fname = parse.urlsplit(response.url).netloc
    try:
        if not os.path.exists(fname):
            os.makedirs(fname)
    except InvalidFilename:
        print("the filename could not be used, use another")

    save_page_to_file(response, fname)

    links = set()
    for link in links_on_page:
        xs = parse.urlsplit(link)
        links.add(xs.scheme + "://" + xs.netloc + xs.path)

    for link in links:
        response, _ = req(link)
        save_page_to_file(response, fname)


if __name__ == "__main__":
    get_url("http://docs.python-requests.org/en/master/")
