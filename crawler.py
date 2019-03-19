from bs4 import BeautifulSoup
from urllib.request import urlopen
import sys
import time
import re

def search(searchText):
    url = 'https://arxiv.org/search/?searchtype=all&size=100&order=&query=' + searchText
    html = urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')

    paper_info = []
    words_count = {}
    stop_words = get_stop_words('./stop_words.txt')
    paper_urls = [p.a['href'] for p in soup.find_all('p', 'list-title')]
    for p_url in paper_urls:
        paper_html = urlopen(p_url).read()
        paper_soup = BeautifulSoup(paper_html, 'html.parser')

        # paper information
        title = paper_soup.find('h1', 'title mathjax').contents[1]
        authors = ';'.join([a.string for a in paper_soup.find('div', 'authors').find_all('a')])
        paper_info.append(p_url)
        paper_info.append(title)
        paper_info.append(authors)

        # words count
        words = re.sub("[;~!@#$%^&*><.?,()\n]", '', paper_soup.find('blockquote', 'abstract mathjax').contents[1]).split(' ')
        for w in words:
            if w not in stop_words:
                if not w == '':
                    word = w.lower()
                    words_count[word] = words_count.get(word, 0) + 1

        time.sleep(0.1)

    # output paper_info.txt
    with open('paper_info.txt', 'w', encoding='utf-8') as f:
        for line in paper_info:
            f.write(line + '\n')

    # output frequent_words.txt
    with open('frequent_words.txt', 'w', encoding='utf-8') as f:
        for i, w in zip(range(50), sorted(words_count.items(), key=lambda d: -d[1])):
            f.write('%s %d\n' % (w[0], w[1]))

    
def get_stop_words(filename):
    with open(filename, 'r') as f:
        stop_words = f.read().splitlines()
    return stop_words

if __name__ == '__main__':
    if len(sys.argv) > 1:
        searchText = sys.argv[1]
    else:
        searchText = 'data+science'
    search(searchText)