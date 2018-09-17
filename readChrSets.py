import ast


# Adds a character set to dictionary.
def add_to_set(title, span, chrSets):
    if '(ctd.)' in title:  # If character set is a continuation of a previous set then join their intervals.
        title = title.strip(' (ctd.)')
        start, end = chrSets[title][-1]
        for interval in span:
            if interval[0] - end == 1:
                chrSets[title][-1] = (start, interval[1])
            else:
                chrSets[title].append(interval)
    else:
        chrSets[title] = span

    return chrSets


# Reads character sets from 'chrSets.txt' into a dictionary.
def load_sets():
    chrSets = {}
    with open('chrSets.txt', 'r') as f:
        for line in f:
            line = line.strip('\n')
            line = line.split(';')
            span = ast.literal_eval(line[2])
            title = line[0]
            chrSets = add_to_set(title, span, chrSets)

    return chrSets