import requests
import io
from bs4 import BeautifulSoup


def get_cell(tag):
    for s in tag.stripped_strings:
        if 'Controls' in s:
            temp = s.split()[-2:]
            return ' '.join(temp)
        else:
            return s


def get_spans(tr):
    tr += 2
    th = table[tr].find('th')
    start = list(get_cell(th))
    start[-1] = '0'
    start = ''.join(start)

    td = table[tr+1].find_all('td')
    while len(td) not in (0, 1):
        tr += 1
        td = table[tr+1].find_all('td')

    th = table[tr].find('th')
    end = list(get_cell(th))
    end[-1] = 'F'
    end = ''.join(end)
    return [tr, (start, end)]


def get_blanks(tr):
    blanks = []
    i = 0
    tr += 2
    td = table[tr].find_all('td')
    while len(td) not in (0, 1):
        for cel in td:
            if cel.find('span') is None:
                blanks.append(i)
            i += 1
        tr += 1
        td = table[tr].find_all('td')
    return blanks


BMPref = ['{}000-{}FFF'.format(('%01X' % i), ('%01X' % i)) for i in range(16)]

url = 'https://en.wikibooks.org/wiki/Unicode/Character_reference/' + BMPref[0]

html = requests.get(url).text

soup = BeautifulSoup(html, "html.parser")

table = soup.select_one("div[class*=parser] > table[style^=border]")
table = table.find_all('tr')


f = io.open('chrSet.txt', 'w', encoding="utf-8")

tr = 0
while tr < len(table):
    td = table[tr].find_all('td')
    if len(td) == 1:
        if get_cell(td[0]) != 'Unassigned':
            f.write(get_cell(td[0]) + ' ')
            spans = get_spans(tr)
            f.write(str(spans[1]) + ' ')
            f.write(str(get_blanks(tr)) + '\n')
            tr = spans[0]
    tr += 1
