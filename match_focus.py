import sys
import codecs
import string
import unicodedata
from translate import load_questions


class TranslatedQuestion(object):
    
    def __init__(self, qid, text, alignment):
        self.qid = qid
        self.text = text
        self.alignment = alignment


def load_translations(translations_file):
    translations = []
    with codecs.open(translations_file, "r", "utf-8") as f:
        for line_n, line in enumerate(f):
            try:
                qid, text, focus = line.strip().split("\t")
                translation = TranslatedQuestion(qid, text, focus)
                translations.append(translation)
            except Exception:
                pass    
    return translations


def main(argv=sys.argv):
    #questions_file = "path/to/file"
    questions_file = "question-focus-classifier-on-trec.txt"
    translations_file = "question-focus-tr.txt"
    
    output = "question-focus-classifier-on-trec-ita.txt"
    
    
    questions = load_questions(questions_file)    
    print "loaded %d questions" % (len(questions))
    
    translations = load_translations(translations_file)
    print "loaded %d translations" % (len(translations))
    
    qids = [translation.qid for translation in translations]
    questions = [question for question in questions if question.qid in qids]
    
    question_translations = zip(questions, translations)
    print "found %d <question, translation> pairs" % (len(question_translations))
    
    out = codecs.open(output, "w", "utf-8")
    
    matched_focus_n = 0
    
    for question, translation in question_translations:
        translated_focus = match_focus(question.text, translation.text, question.focus, translation.alignment)
        out.write(translation.qid + "\t" + translation.text + "\t" + translated_focus + "\n")
    out.close()
        
    print "unmatched_focus_n: ", len(translations) - matched_focus_n
    

def overlap(t1, t2):
    return set(range(*t1)) & set(range(*t2))
    

def find_most_likely_match(matches, start, end):
    dists = []
    for match in matches:
        src, target = match.split("-")
        #print "dist(" + src + " ->" + str(start) + ":" + str(end) + "):",
        src = tuple(map(int, src.split(":")))
        
        dist = abs(src[0] - start) + abs(src[1] - end)
        
        
        dists.append(dist if overlap((start, end), src) else sys.maxint)
        
    #print "dists:", dists
        
    pos = dists.index(min(dists))
    return matches[pos].split("-")[1]
        

    

def match_focus(question, translation, focus, alignment):   
    ix = question.index(focus)
    begin, end = ix, ix + len(focus)
    
    #print question
    #print translation
    #print alignment
    
    #print "original focus: {0}".format(focus)
    #print "focus spanning from {0} to {1}: {2}".format(begin, end, question[begin:end])
    
    matches = dict([align.split("-") for align in alignment.split()])
    
    key = str(begin) + ":" + str(end)
    
    #translation = strip_accents_unicode(translation)
    
    try:
        lx, rx = map(int, matches[key].split(":"))
    except Exception:
        lx, rx = map(int, find_most_likely_match(alignment.split(), begin, end).split(":"))
        
        """Shifting the lx index for taking into account the unicode accents!"""
        ilx = lx
        lx = 0
        i = 0
        while lx < ilx:
            if not unicodedata.combining(translation[i]):
                lx += 1 
            i += 1
        
        """Shifitng the rx index for taking into account the unicode accents!"""
        irx = rx
        rx = 0
        i = 0
        while rx < irx:
            if not unicodedata.combining(translation[i]):
                rx += 1
            i += 1
    tr_focus = translation[lx:rx + 1].strip(string.punctuation)
    
    #print "tr focus spanning from {0} to {1}: {2}".format(lx, rx, tr_focus.strip)
    
    return tr_focus

        
def strip_accents_unicode(s):
    return "".join([c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c)])
    
    
def print_alignment(a, b, alignment):
    for align in alignment.split():
        src, target = align.split("-")
        src = tuple(map(int, src.split(":")))
        target = tuple(map(int, target.split(":")))
        
        #print "src:", src
        #print "target:", target
        
        print a[src[0]:src[1] + 1] + " -> " +  b[target[0]:target[1] + 1]
    

def test():
    question = "When did the story of Romeo and Juliet take place?"
    focus = "place"
    translation = "Quando la storia di Romeo e Giulietta avvenuta?"
    alignment = "0:3-0:5 5:7-38:45 9:11-7:8 13:17-10:15 19:20-17:18 22:26-20:24 28:30-26:26 32:37-28:36 39:48-38:45 49:49-46:46"
    
    print_alignment(question, translation, alignment)
    
    print match_focus(question, translation.decode("utf-8"), focus, alignment)


if __name__ == "__main__":
    """
    question = "Who sang \"Tennessee Waltz\"?"
    focus = "Tennessee"
    translation = "Chi ha cantato \"Tennessee Waltz\"?"
    alignment = "0:2-0:2 4:7-4:13 9:18-15:24 20:26-26:32"
    
    match_focus(question, translation, focus, alignment)
    """
    #main()
    pass
