from bs4 import BeautifulSoup
from collections import OrderedDict
import requests

config = OrderedDict(
    header={"User-Agent" :"Mozilla/5.0 (X11; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0"},
    link="https://www.uta-net.com/song/289539/",
    tags=["<br/>", "<div", "</div>"],
)

def get_html(url):
    """
    :input url: The url to retrieve
    :output: The html of the page
    """
    r = requests.get(url, config["header"])
    return r.text

def extract_kashi(str_content):
    """
    :input str_content: The string which you want to extract content from
    :output: The lyrics in a list
    """
    ret = []
    for i in iter(str_content.splitlines()):
        lyric = True
        # TODO: Probably a better way around this
        for tag in config["tags"]:
            if tag in i:
                lyric = False
                continue

        if lyric:
            ret.append(i.replace("\u3000", " ").replace("\u200b", " "))

    return ret
                
def get_kashi(content):
    """
    :input content: the html content of the page
    :output: The lyrics in a list
    """
    soup = BeautifulSoup(content, "lxml")
    return extract_kashi(soup.find("div", {"id": "kashi_area"}).prettify())

def pretty_print_kashi(kashi):
    """
    Pretty prints the kashi
    :input kashi: the kashi
    """
    for line_no, kotoba in enumerate(kashi):
        print("{}: {}".format(line_no+1, kotoba))

def get_artist(content):
    """
    :input content: the html content of the page
    :output: A string containing the artist
    """
    soup = BeautifulSoup(content, "lxml")
    return soup.find("span", {"itemprop": "byArtist name"}).contents

h = get_html(config["link"])
pretty_print_kashi(get_kashi(h))
print(get_artist(h))
