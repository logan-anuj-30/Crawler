from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import urlparse


class Spider:
    wrong = ['cover', 'login', 'signup','monitor','tab','refrigerator','guru','profile', 'tv', 'sticker', 'glass', 'refurbished', 'charger', 'ipad', 'macbook',
             'laptop', 'watch', 'trolly', 'shockproof', 'power', 'bank', 'cosmetics', 'band', 'adapter', 'case',
             'tempered', 'use', 'back', 'protector', 'signin', 'review', 'earphone', 'headphone']
    url = ''
    domain_name = ''
    queue = set()
    crawled = set()
    search_results = set()
    mongo_export = []
    query = []



    def __init__(self, url, domain_name, query):
        Spider.domain_name = domain_name
        Spider.url = url
        Spider.queue.add(url)
        Spider.query = query
        print('Amazon Process')
        Spider.crawl_page('Process', url, 0)



    @staticmethod
    def crawl_page(thread_name, page_url, search_code):
        page_url=page_url.split('#product')[0]
        page_url=page_url.split('?_')[0]

        if page_url not in Spider.crawled:
            url = Spider.check_URL(page_url, search_code)
            if (len(url) > 5):
                Spider.gather_links(url, thread_name)

            if search_code==0:
                Spider.crawled.add(page_url)
                Spider.queue.remove(page_url)
            else:
                Spider.crawled.add(page_url)




    @staticmethod
    def gather_links(url, thread_name):
        try:
            html = requests.get(url)
        except Exception as e:
            print('Error in requesting Amazon(Spider) : ' + str(e))
            return

        text = html.text
        soup = BeautifulSoup(text, 'html.parser')
        links = soup.find_all('a')

        print('.')
        for i in soup.find_all('span', {'id': 'productTitle'}):
            if str(i) != 'None':
                msg = str(i.string).lower().strip()

                for j in Spider.wrong:
                    if msg.find(j) != -1:
                        return

                print(thread_name + ' Amazon Found : ' + msg + '\n' + url + '\n\n')

                x = re.sub(r'gb', ' gb', msg)
                msg = Spider.format_query(x)

                Spider.mongo_export.append({'name': msg, 'url': url.strip()})

                count = 0
                for j in range(len(Spider.query)):
                    if Spider.query[j] not in msg:
                        count = 1
                        break
                if count == 0:
                    Spider.search_results.add(url)
                    return

        for link in links:
            u = str(link.get('href'))
            if u not in Spider.crawled and u not in Spider.queue:
                Spider.queue.add(u)



    @staticmethod
    def check_URL(url, search_code):
        lower = url.lower()

        for i in Spider.wrong:
            if lower.find(i) != -1:
                return ''

        tuplle = urlparse(url)  # this will return a tuple of 6 elements

        if tuplle.netloc == '':  # checking weather the URl is relative or not
            url = Spider.domain_name + url

        if url.find('amazon.in') == -1:  # to avoid outside links
            return ''

        if search_code == 0:
            return url


        if lower.find(Spider.query[0]) != -1:
            return url
        else:
            return ''



    @staticmethod
    def format_query(query):
        l = []
        q = query.lower()
        query = re.sub('[-,/@()]', ' ', q)
        query = query.split()
        for i in query:
            l.append(i.strip())
        return l
