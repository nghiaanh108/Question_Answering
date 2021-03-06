from googleapiclient.discovery import build
from numpy import random
import requests
from bs4 import BeautifulSoup
import timeout_decorator
from nltk import sent_tokenize
from multiprocessing import Pool
import re
import sys
try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")

api_key = ['AIzaSyB4stN8eqW0ci3lIEJnx2ZTxQ-n65Vh5bY',
           'AIzaSyDlAhHd-kyrisR0uiJI4tBDHSUQEvIHCyA',
           'AIzaSyA6wNFY3uD9TelHYmzvIu5APhjweIMcnd0',
           'AIzaSyBu6s7HmBmhVEN0_ECEN7_F38egUKOhsbc',
           'AIzaSyBhuF-kGVbgibg6fk4DplpVbBeSxQytXLc',
           'AIzaSyA7ejsk_W84efiUIRwwMzEil0LZltNw-a8',
           'AIzaSyBj9UEWJGZfIt1ce9BwopoBKoh-k3tv8wY',
           'AIzaSyCeIqkVUR53QHNhsa5jp3GvY2uTicEjApQ',
           'AIzaSyCod6nlTne0tqUttJWJKrYt8XdMofJQ5d4',
           'AIzaSyBtxMQRjNRWTPijCFpTWIx9Vsmqn6LvjWs']

Custom_Search_Engine_ID = "649dd6e1fe1ffe13e"

# api_key = ['AIzaSyCIK5w6f4MrhgYzNPCVkMFrQxN_IQ_KO5w', 
#            'AIzaSyAF8jAPuv8oiJfJMKs_zFqUxGh11BT6OG4',
#            'AIzaSyBn3rmVMyn18jOc_K24BxXxewKBSMwZ7W0',
#            'AIzaSyCYZt6vYMXhTn3dykAtVi6KrkQ1b30rd0c',
#            'AIzaSyBLNAMh9TT6GGuRD1cxXM2X2YovlI-wyx8',
#            'AIzaSyDOMcbV8el6aAPay-I2t50n3MeB4YxV-nY',
#            'AIzaSyBvwz1-7wFsDKHAtPvE_ScQSf7Tbj_GXr4',
#            'AIzaSyC354FqnOpQUy69OFVhLd48FcxNXRFC0SQ',
#            'AIzaSyDx7H9lTj3pNVcxUXploZ9LdW_87_Ia4bs',
#            'AIzaSyA0xioeFHXFxWo4Z5yUDxI1hFMtfRU_KFU']

# Custom_Search_Engine_ID = "005336700654283051786:1mzldt1husk"

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

@timeout_decorator.timeout(3)
def ggsearch(para):
    try:
        i = para[0]
        service = para[1]
        query = para[2]
        if (i == 0):
            res = service.cse().list(q=query,cx = Custom_Search_Engine_ID, gl ='vn', 
                                     googlehost = 'vn', hl = 'vi').execute()
        else:
            res = service.cse().list(q=query,cx = Custom_Search_Engine_ID,num=10,start = i*10, gl ='vn', 
                                     googlehost = 'vn', hl = 'vi').execute()
        return res[u'items']
    except:
        return []

@timeout_decorator.timeout(7)
def getContent(url):
    try:
        html = requests.get(url, timeout = 4)
        tree = BeautifulSoup(html.text,'lxml')
        for invisible_elem in tree.find_all(['script', 'style']):
            invisible_elem.extract()

        paragraphs = [p.get_text() for p in tree.find_all("p")]

        for para in tree.find_all('p'):
            para.extract()

        for href in tree.find_all(['a','strong']):
            href.unwrap()

        tree = BeautifulSoup(str(tree.html),'lxml')

        text = tree.get_text(separator='\n\n')
        text = re.sub('\n +\n','\n\n',text)

        paragraphs += text.split('\n\n')
        paragraphs = [re.sub(' +',' ',p.strip()) for p in paragraphs]
        paragraphs = [p for p in paragraphs if len(p.split()) > 10]

        for i in range(0,len(paragraphs)):
            sents = []
            text_chunks = list(chunks(paragraphs[i],100000))
            for chunk in text_chunks:
                sents += sent_tokenize(chunk)

            sents = [s for s in sents if len(s) > 2]
            sents = ' . '.join(sents)
            paragraphs[i] = sents

        return '\n\n'.join(paragraphs)
    except:
        print('Cannot read ' + url, str(sys.exc_info()[0]))
        return ''


class GoogleSearch():
    __instance = None
    
    @staticmethod 
    def getInstance():
        """ Static access method. """
        if GoogleSearch.__instance == None:
            GoogleSearch()
        return GoogleSearch.__instance
    
    def __init__(self):
        if GoogleSearch.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.pool = Pool(4)
            GoogleSearch.__instance = self
            
    def search(self, question):
        service = build("customsearch", "v1", developerKey=api_key[random.randint(0,10)])
        pages_content = self.pool.map(ggsearch,[(i, service, question) for i in range(0,2)])
        print('pages_content1:', pages_content)
        pages_content = [j for i in pages_content for j in i]
        print('pages_content:', pages_content)
        pages_content = pages_content[:10]
        document_urls = set([])
        for page in pages_content:
            if 'fileFormat' in page:
                continue
            document_urls.add(page[u'link'])
        document_urls = list(document_urls)
        # document_urls = set([])
        # for j in search(question, tld="com", lang='vi', num=10, stop=10, pause=0):
        #   document_urls.add(j)
        # document_urls = list(document_urls)
        print('document_urls: ', document_urls)

        gg_documents = self.pool.map(getContent, document_urls)
        gg_documents = [d for d in gg_documents if len(d) > 20]
        print('gg_documents: ', gg_documents)

        return document_urls, gg_documents




