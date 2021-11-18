from underthesea import word_tokenize
from underthesea import ner
from nltk import sent_tokenize
from bs4 import BeautifulSoup
import requests
import sys
try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")


stopwords = "bị bởi cả các cái cần càng chỉ chiếc cho chứ chưa chuyện có cứ của cùng cũng đã đang đây để đến đều điều do đó được dưới gì khi không là lại lên lúc mà mỗi một này nên nếu ngay nhiều như nhưng những nơi nữa phải qua ra rằng rằng rất rất rồi sau sẽ so sự tại theo thì trên trước từ từng và vẫn vào vậy vì việc với vừa"
puct_set = set([c for c in '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'])

class Passage:
    def __init__(self,string,rank,num_key):
        self.sent = string            #sentences
        self.ner = []                 #named entities
        self.num_key = num_key        #number of match keywords
        self.len_long_seq = 0         #length of longest exact sequence of question keywords
        self.rank = rank              #rank of own document
        self.ngram_overlap = 0        #ngram overlap question
        self.proximity = 0            #shortest keywords that cover all keywords
        self.score = 0                #Overall score

def tokenize(text):
    sents = sent_tokenize(text)
    sents = [word_tokenize(s,format = 'text') for s in sents]
    return sents

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def noiseSent(sent):
    if len(sent.split()) <= 3 or len(sent.split()) > 100:
        return True
    
    if len(sent) <= 30:
        return True
    
    if all(ord(c) < 128 for c in sent):
        return True
    
    if not any(c.isalpha() for c in sent):
        return True

def keywords_extraction(sentences):
    sent = sentences.lower()
    sent = sent.split()
    sent = [s for s in sent if s not in stopwords and s not in puct_set]
    return sent

def getContent(url, keywords):
    try:
        rank = int((0 + 5)/5) - 1 
        passages = []
        html = requests.get(url, timeout = 4)
        tree = BeautifulSoup(html.text,'lxml')
        for invisible_elem in tree.find_all(['script', 'style']):
            invisible_elem.extract()

        sents = []
        text_chunks = list(chunks(tree.get_text(),100000))
        for text in text_chunks:
            sents += tokenize(text)
        
        for sent in sents:
            sent = sent.strip()
            if not noiseSent(sent):
                sent_keywords = keywords_extraction(sent)
                num_overlap_keywords = len(set(sent_keywords) & set(keywords))
                if num_overlap_keywords > 0:
                    passages.append(Passage(sent,rank,num_overlap_keywords))
                    
        return passages
    except:
        print('Cannot read ' + url, str(sys.exc_info()[0]))
        return ''
def reb(li):
    b = []
    for item in li:
        text = ''
        for pas in item:
            text = text + pas.sent
        b.append(text)
    return b

def reurl_li(questions_, keywords):
    li = []
    urls = []
    for j in search(questions_, tld="com", lang='vi', num=5, stop=5, pause=0):
        a = getContent(j, keywords)
        li.append(a)
        urls.append(j)
    return li, urls