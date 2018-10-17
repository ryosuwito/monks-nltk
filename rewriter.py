import bs4 as bs
from urllib2 import urlopen, Request
import re
import nltk
import heapq
import requests
import time

def rechanger(summary):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = nltk.sent_tokenize(summary.encode('utf-8').replace('...','.'))
    pathI = '1'
    premium = 'true'
    useBad = 'true'
    userID= 'N/A'
    urls = 'https://api.quillbot.com/api/singleParaphrase'
    results = []
    print(sentences)
    for txt in sentences:
        payload = {'userID':userID, 'pathI':pathI, 'premium':premium, 'useBad':useBad, 'text':txt}
        response = requests.get(urls, params=payload)
        print(response.text)
        json = response.json()
        try:
            print(json[0]['paras'][0])
            results.append(json[0]['paras'][0])
        except:
            print('###### FAIL \########')
            pass
        time.sleep(2)
    
    rewrited_text = ' '.join(results)
    return rewrited_text

def rewriter(summary):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = nltk.sent_tokenize(summary.encode('utf-8').replace('...','.'))
    pathI = '1'
    premium = 'true'
    useBad = 'true'
    userID= 'N/A'
    urls = 'https://api.quillbot.com/paraphrase'
    results = []
    print(sentences)
    for txt in sentences:
        payload = {'userID':userID, 'pathI':pathI, 'premium':premium, 'useBad':useBad, 'text':txt}
        response = requests.get(urls, params=payload)
        print(response.text)
        json = response.json()
        try:
            print(json['beams'][0])
            results.append(json['beams'][0])
        except:
            print('###### FAIL \########')
            pass
        time.sleep(2)
    
    rewrited_text = ' '.join(results)
    return rewrited_text

def summarizer(urls):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    req = Request(urls, headers=hdr)
    scraped_data = urlopen(req)
    article = scraped_data.read()

    parsed_article = bs.BeautifulSoup(article, 'lxml')

    paragraphs = parsed_article.find_all('p')

    article_text = ''

    for p in paragraphs:
        article_text += p.text

    article_text = re.sub(r'\[[0-9]*\]',' ', article_text)
    article_text = re.sub(r'\s+', ' ', article_text)

    formatted_text = re.sub('[^a-zA-Z]', ' ', article_text)
    formatted_text = re.sub(r'\s+', ' ', formatted_text)

    sentence_list = nltk.sent_tokenize(article_text)
    
    return article_text
    """
    stopwords = nltk.corpus.stopwords.words('english')

    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    maximum_frequency = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequency)

    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 160:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]

    summary_sentences = heapq.nlargest(770, sentence_scores, key=sentence_scores.get)

    summary = ' '.join(summary_sentences)
    return summary
    """
    
urls_list = ''
print('loading urls list')
with open('urls_source.txt') as f:
    urls_list = f.read().splitlines()

summaries = []
print('begin rewriting urls')
for url in urls_list:
    print('begin summarizing %s'%(url))
    summary = summarizer(url)
    url_name = url.split('/')[-1]
    print('write summarized text into %s'%(url_name))
    with open('results/%s.txt'%url_name, 'w') as f:
        f.write('Original: \n\n')
        f.write(summary.encode('utf-8'))
        f.write('Source: \n\n %s \n'%(url_name))
    
    print('begin rewriting %s'%(url))
    rewriten_text = rewriter(summary)

    rewriten_text = rechanger(rewriten_text)

    rewriten_text = rewriter(rewriten_text)

    with open('results/%s.txt'%url_name, 'a') as f:
        f.write('Result: \n\n')
        f.write(rewriten_text.encode('utf-8'))

    timer = 160
    i = 1
    print('sleep for %s second'%timer)
    while i <= timer:
        time.sleep(1)
        print i
        i+=1

print('done')

