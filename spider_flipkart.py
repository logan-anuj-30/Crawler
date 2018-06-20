from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import re


class Spider:
    wrong = ['cover', 'login', 'signup','headset','cabel','laptop', 'tv', 'charger', 'ipad', 'macbook', 'glass', 'watch', 'trolly',
             'shockproof', 'power', 'bank', 'cosmetics', 'band', 'adapter', 'case', 'tempered', 'use', 'back',
             'protector', 'signin', 'review', 'earphone', 'headphone']

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
        print('Flipkart Process')
        Spider.crawl_page('Process Flipkart', url, 0)

    @staticmethod
    def crawl_page(thread_name, page_url, search_code):
        page_url=page_url.split('&lid=')[0]
        page_url=page_url.split('?pid=')[0]

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
            text = html.text
        except Exception as e:
            print('Error in requesting Flipkart(Spider) : ' + str(e))
            return
        soup = BeautifulSoup(text, 'html.parser')

        links = soup.find_all('a')
        print('.')
        for i in soup.find_all('span', {'class': '_35KyD6'}):
            if str(i) != 'None':
                msg = str(i.get_text()).lower().strip()

                for i in Spider.wrong:
                    if msg.find(i) != -1:
                        return

                print(thread_name + ' Flipkart Found : ' + msg + '\n' + url + '\n\n')

                msg = Spider.format_query(msg)
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

        tuplle = urlparse(url)

        if tuplle.netloc == '':
            url = Spider.domain_name + url

        if url.find('flipkart.com') == -1:
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
