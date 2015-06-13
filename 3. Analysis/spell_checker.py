import re, collections, csv, ast
from unidecode import unidecode
import sys

def words(text): return re.findall('[0-9a-z]+', text.lower())

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train(words(file('big.txt').read()))

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)

def main(f, grouping):

    wrong = {}
    for i in f:
        for t in ast.literal_eval(i['tags']):
            tags = []
            t.encode('ascii', 'ignore')
            tags.append(t.lower().replace(',', '').replace('.', '').replace('\'',''))
            for phrase in tags:
                for word in phrase.split(' '):
                    corrected = correct(unidecode(word))
                    if word != corrected:
                        # if sum(1 for x,y in zip(t, corrected) if x != y) > 1: # more than one letter different
                        # if "".join(t.split()) != corrected:
                        if not word.isdigit():
                            if len(i[grouping]) > 1:
                                if not i[grouping] in wrong:
                                    wrong[i[grouping]] = 1
                                else:
                                    wrong[i[grouping]] += 1
    print wrong
    with open('output.csv', 'ab') as f:
        for key, value in wrong.iteritems():
                w = csv.writer(f)
                w.writerow([key, value])

if __name__=="__main__":
    # csv file for analysis
    with open(sys.argv[1], 'rU') as csvFile:
        f = csv.DictReader(csvFile, dialect='excel')

        # the clustering at which you want to group counts of misspelled tags, ie. locale or region or county, etc.
        grouping = sys.argv[2]

        main(f, grouping)
