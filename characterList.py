# Writes to file 'characters.txt' a list of all printable characters from Unicode's BMP (ver 11.0).
# Can be reconfigured to filter out characters based on category, character set.

import unicodedata
import readChrSets


# Checks if unicode character is in specified character sets.
def in_set(index, setFilter):
    for s in setFilter:
        for interval in chrSet[s]:
            if interval[0] <= index <= interval[1]:
                return True
    return False


# Unicode Categories
# More information at http://www.fileformat.info/info/unicode/category/index.htm
control     = ('Cc', 'Cf', 'Cn', 'Co', 'Cs')
separator   = ('Zl', 'Zp', 'Zs')
letter      = ('LC', 'Ll', 'Lm', 'Lo', 'Lt', 'Lu')
number      = ('Nd', 'Nl', 'No')
mark        = ('Mc', 'Me', 'Mn')
punctuation = ('Pc', 'Pd', 'Pe', 'Pf', 'Pi', 'Po', 'Ps')
symbol      = ('Sc', 'Sk', 'Sm', 'So')


# Character Sets and Ranges
# More information at https://en.wikipedia.org/wiki/List_of_Unicode_characters.
chrSet = readChrSets.load_sets()


# Filters
catFilter = control + separator
setFilter = ['Latin Extended-A', 'Greek and Coptic']


# Gets unicode characters based on filters and writes them to file 'characters.txt'.
with open('characters.txt', 'w', encoding="utf-8") as f:
    f.write('    index    code     character    category   name\n')

    c = 0
    for i in range(0, 65536):
        if unicodedata.category(chr(i)) not in catFilter:
            if in_set(i, setFilter):
                glyph = chr(i)
                code = r"\u%04X" % i
                cat = unicodedata.category(glyph)
                name = unicodedata.name(glyph)
                s = '{}   {}      {}        {}       {}         {}\n'\
                    .format(c, i, code, glyph, cat, name)
                f.write(s)
                c += 1
