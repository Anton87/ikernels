import string
import codecs
import msmt
import sys
import re



import unicodedata

client_id = "msmt-test"
client_secret = "UZqXurE3aLEFYF/umR4tGbT11mH61wznNTU2n/ATbyc="


class Question:

    def __init__(self, qid, text, focus):
        self.qid = qid
        self.text = text
        self.focus = focus
        

def load_questions(src_file):
    questions = []
    
    with codecs.open(src_file, "r", "utf-8") as f:
        for line in f:
           line = line.strip()
           sp1, sp2 = line.index(" "), line.rindex(" ")
           
           qid = line[:sp1]
           focus = line[sp2 + 1:]
           text = line[sp1 + 1:sp2]
           
           question = Question(qid, text, focus)
           questions.append(question)
    return questions
    
        
def tr():
    src_file = "question-focus-classifier-on-trec.txt"
    
    QUESTIONS_PER_REQUEST = 1
    
    questions = load_questions(src_file)
    
    start = 200
    end = 250
    
    access_token = msmt.get_access_token(client_id, client_secret)
    
    iter_n = (end - start) / QUESTIONS_PER_REQUEST
    
    print "iter_n:", iter_n
    
    dest_file = "4.txt"
    
    out = codecs.open(dest_file, "w", "utf-8")
    
    for i in range(iter_n): 
    
        print "iter:", i
        
        qbegin = start + i * QUESTIONS_PER_REQUEST
        
        qend = qbegin + QUESTIONS_PER_REQUEST
        
        qids = [question.qid for question in questions[qbegin:qend]]
        
        print "writing question from {0} to {1}... ".format(qbegin, qend)
        
        texts = [question.text for question in questions[qbegin:qend]]
        
        resp = msmt.translateArray(access_token, texts, "it", "en")
        
        translations = msmt.get_tr(resp)
        
        alignments = msmt.get_alignment(resp)
        
        print "len(alignments):",len(alignments)
        
        length = len(translations)
        print "len(translations):", len(translations)
        
        for qid, translation, alignment in zip(qids, translations, alignments):
            line = qid + "\t" + translation + "\t" + alignment + "\n"
            out.write(line)
            
    out.close()


def main(argv=sys.argv):
    src_file = "question-focus-classifier-on-trec.txt"
    
    #dest_file = "1.txt"
    
    #access_token = msmt.get_access_token(client_id, client_secret)
    
    QUESTIONS_PER_REQUEST = 25
    
    #out = codecs.open(dest_file, "w", "utf-8")
    
    questions = load_questions(src_file)
    print len(questions)
    
    access_token = msmt.get_access_token(client_id, client_secret)
           
    iter_n = len(questions) / QUESTIONS_PER_REQUEST 
    #iter_n = 4
        
    print "iter_n:", iter_n
        
    for i in range(iter_n + 1):
    
        print "iter:", i
        
        dest_file = "3.txt"
        
        out = codecs.open(dest_file, "w", "utf-8")
    
        start = i * QUESTIONS_PER_REQUEST 
        end = min(start + QUESTIONS_PER_REQUEST, len(questions))
            
        print "writing sentence from {0} to {1}...".format(start, end)
        
        texts = [question.text for question in questions[start:end]]
        
        resp = msmt.translateArray(access_token, texts, "it", "en")
        
        translations = msmt.get_tr(resp)
        
        alignments = msmt.get_alignment(resp)
        
        print "len(alignments):",len(alignments)
        
        length = len(translations)
        print "len(translations):", len(translations)
        
        for num, (translation, alignment) in enumerate(zip(translations, alignments)):
            line = questions[start + num].qid + "\t" + translation + "\t" + alignment + "\n"
            out.write(line)
            
        out.close()
    
    """
    start = iter_n * QUESTIONS_PER_REQUEST
    end = len(questions)
            
    print "writing sentence from {0} to {1}...".format(start, end)
        
    texts = [question.text for question in questions[start:end]]
        
    resp = msmt.translateArray(access_token, texts, "it", "en")
        
    translations = msmt.get_tr(resp)
        
    alignments = msmt.get_alignment(resp)        
    print "len(alignments):",len(alignments)
        
    length = len(translations)
    print "len(translations):", len(translations)
        
    for num, (translation, alignment) in enumerate(zip(translations, alignments)):
        line = questions[start + num].qid + "\t" + translation + "\t" + alignment + "\n"
        out.write(line)
    """
    
    
    


    
def find_it_focus():   
    #qid = 1396
    question = "What is the name of the volcano that destroyed the ancient city of Pompeii?"
    focus = "name"    
    tr = "Qual e il nome del vulcano che distrusse l'antica citta di Pompei?"
    alignments = "0:3-0:3 5:6-5:5 8:10-7:8 12:15-10:13 17:18-15:17 24:30-19:25 32:35-27:29 37:45-31:39 51:57-41:48 59:62-50:54 64:65-56:57 67:73-59:64 74:74-65:65"
    
    ix = question.index(focus)
    
    begin, end = ix, ix + len(focus) - 1
    
    matches = dict([align.split("-") for align in alignments.split()])
    
    key = str(ix) + ":" + str(ix + len(focus) -1)
     
    lx, rx = map(int, matches[key].split(":"))
    rx = rx + 1
    
    begin = 0
    end = 0
    
    n_alpha = 0
    normalized_tr = "".join([c for c in unicodedata.normalize('NFKD', tr.decode("utf-8")) if not unicodedata.combining(c)])
         
    print [c for c in normalized_tr]        
            
        
    print normalized_tr
    
        
            
    
    print "\"" + normalized_tr[lx:rx + 1] + "\""
    
    
    


    
if __name__ == "__main__":
    find_it_focus()
    
    
        


        
        
    
        
    
    
    
    
    
    
    
    

