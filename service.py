from models import Collection, ComicCollection, Comic
import requests
from bs4 import BeautifulSoup
import re
import unidecode

pattern = re.compile('[\W_]+')


def cleanText(txt):
    return unidecode.unidecode(pattern.sub('', txt)).upper()


def fillData():
    for col in Collection.select():
        req = requests.get(col.url)
        print(f'Reading {col.title}')
        if req.status_code == 200:
            soup = BeautifulSoup(req.content, 'html.parser')
            for i, td in enumerate(soup.findAll('td', {'class': 'column-2'})):
                comicid = cleanText(td.text)

                if comicid != '' and Comic.get_or_none(id=comicid) == None:
                    Comic.create(id=comicid, raw_name=td.text.strip())
                    print(f'Created Comic {td.text.strip()}')

                if comicid != '' and ComicCollection.get_or_none(comic=comicid, collection=col.id) == None:
                    ComicCollection.create(
                        comic=comicid, collection=col.id, order=i)
                    print(f'Created Comic On Colletion {comicid} - {col.id} - {i}')
        else:
            print(f'Invalid Status Code {req.status_code}')


if __name__ == '__main__':
    fillData()