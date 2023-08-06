import urllib.request as urllib
from bs4 import BeautifulSoup
import re
import unshortenit

class AnimeOp:

    def __init__(self):
        self.url = ''
        self.first = ''
        self.last = ''
        self.fname = ''

    def link(self):
        resp = urllib.urlopen(self.url)
        soup = BeautifulSoup(resp.read())

        link = soup.find_all('a', href=re.compile(r'http:\/\/adf.ly\/[\s\S].....'), text=re.compile(r'\d'))
        i = 0
        for value in link:
            i += 1
            if (i > self.first) and (i < self.last):
                unshortened_uri, status = unshortenit.unshorten_only(value['href'])
                print(unshortened_uri, value.contents[0])
                with open(self.fname + ".txt", "a") as myfile:
                    myfile.write(unshortened_uri + " - " + value.contents[0] + "\n")
            else:
                pass
        return "Done!"
