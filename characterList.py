# Writes to file 'characters.txt' a list of all printable characters from Unicode's BMP (ver 11.0)
# Can be reconfigured to filter out any characters based on category, character set

import unicodedata
import io


# Checks if ith unicode character is in the range of specified character sets
def setCheck(i, setList):
    for s in setList:
        if chrSet[s][0] <= i <= chrSet[s][1]:
            return True
    return False


# Unicode Categories  ( more information: http://www.fileformat.info/info/unicode/category/index.htm )
control     = ('Cc', 'Cf', 'Cn', 'Co', 'Cs')
separator   = ('Zl', 'Zp', 'Zs')
letter      = ('LC', 'Ll', 'Lm', 'Lo', 'Lt', 'Lu')
number      = ('Nd', 'Nl', 'No')
mark        = ('Mc', 'Me', 'Mn')
punctuation = ('Pc', 'Pd', 'Pe', 'Pf', 'Pi', 'Po', 'Ps')
symbol      = ('Sc', 'Sk', 'Sm', 'So')


# Character sets and ranges ( from: https://en.wikipedia.org/wiki/List_of_Unicode_characters )
chrSet = {'basic latin': (32, 126),
          'Latin-1 Supplement': (160, 255),
          'Latin Extended-A': (256, 383),
          'Latin Extended-B': (384, 591),
          'Latin Extended Additional': (647, 669)}


# Filter lists
catList = control + separator
setList = ['basic latin', 'Latin Extended Additional']

f = io.open('characters.txt', 'w', encoding="utf-8")
f.write('   index    code     character    category   name\n')

c = 0
for i in range(0, 65536):
    if unicodedata.category(chr(i)) not in catList:
        #if setCheck(i, setList):
            glyph = chr(i)
            code = r"\u%04X" % i
            cat = unicodedata.category(glyph)
            name = unicodedata.name(glyph)
            s = '{}  {}       {}        {}       {}         {}\n'\
                .format(c, i, code, glyph, cat, name)
            f.write(s)
            c += 1

f.close()
