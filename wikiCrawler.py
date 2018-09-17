# Goes through character tables on Wikipedia and gets the names and ranges of character sets
# from Unicode's Basic Multilingual Plane (Unicode 11.0).


import requests
from bs4 import BeautifulSoup


# Gets the string inside a table cell.
def get_cell(tag):
    for s in tag.stripped_strings:
        return s


# Gets unicode range of character segment in table, and its ending row number.
def get_spans(tr):
    tr += 2  # Skips to beginning row of characters, gets starting unicode.
    th = table[tr].find('th')
    start = list(get_cell(th))
    start[-1] = '0'
    start = ''.join(start)

    td = table[tr].find_all('td')  # Goes row by row until hits new segment or end of table.
    while len(td) != 1 and tr+1 < len(table):
        tr += 1
        td = table[tr].find_all('td')

    if get_cell(td[0]) == 'Notes':  # Adjustments for when table ends in a Notes section.
        tr -= 1

    th = table[tr-1].find('th')  # Gets ending unicode.
    end = list(get_cell(th))
    end[-1] = 'F'
    end = ''.join(end)
    return [tr-1, (start, end)]


# Gets list of intervals between blank code points in character segment.
def get_sets(tr):
    tr += 2  # Skips to beginning row of characters, gets starting unicode as integer.
    th = table[tr].find('th')
    u = list(get_cell(th))
    u[-1] = '0'
    u = int(''.join(u), 16)

    sets = []  # Goes through all cells, divides segment into intervals, using blank code points as dividers.
    i = 0
    start = -1
    td = table[tr].find_all('td')
    while len(td) != 1 and tr+1 < len(table):
        if len(td) != 0:
            for cel in td:
                if start < 0 and cel.find('span') is not None:
                    start = i
                elif start >= 0 and cel.find('span') is None:
                    end = i-1
                    sets.append((u + start, u + end))
                    start = -1
                i += 1
        tr += 1
        td = table[tr].find_all('td')
        if (len(td) == 1 or tr+1 >= len(table)) and start >= 0:
            end = i-1
            sets.append((u + start, u + end))
            start = -1
    return sets


BMPref = ['{}000-{}FFF'.format(('%01X' % i), ('%01X' % i)) for i in range(16)]

with open('chrSets.txt', 'a', encoding="utf-8") as f:

    for ref in BMPref:
        url = 'https://en.wikibooks.org/wiki/Unicode/Character_reference/' + ref

        html = requests.get(url).text

        soup = BeautifulSoup(html, "html.parser")

        table = soup.select_one("div[class*=parser] > table[style^=border]")
        table = table.find_all('tr')

        tr = 0
        while tr < len(table):
            td = table[tr].find_all('td')
            if len(td) == 1 and tr+2 < len(table):  # Checks row is the heading to new segment of table.
                if all(s not in get_cell(td[0]) for s in ('Unassigned', 'Surrogate', 'Private', 'Notes')):
                    f.write(get_cell(td[0]) + ';')
                    spans = get_spans(tr)
                    f.write(str(spans[1]) + ';')
                    f.write(str(get_sets(tr)) + '\n')
                    tr = spans[0]
            tr += 1

