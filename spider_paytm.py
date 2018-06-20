import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re


class Spider:
    wrong = ['cover', 'login', 'signup','monitor','guru','metro','tab','refrigerator','fixed','headset','cordless','corded','profile', 'tv', 'sticker', 'glass', 'refurbished', 'charger', 'ipad', 'macbook',
             'laptop', 'watch', 'trolly', 'shockproof', 'power', 'bank', 'cosmetics', 'band', 'adapter', 'case',
             'tempered', 'use', 'back', 'protector', 'signin', 'review', 'earphone', 'headphone']

    domain_name = ''
    queue = set()
    crawled = set()
    search_results = set()
    mongo_export = []
    query = []

    def __init__(self, url, domain_name, query):
        Spider.domain_name = domain_name
        Spider.queue.add(url)
        Spider.query = query
        print('Paytm Process')
        Spider.crawl_page('Process Paytm', url, 0)


    @staticmethod
    def crawl_page(thread_name, page_url, search_code):
        url=page_url.split('?product_id=')[0]
        page_url=url.split('?src=')[0]
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
        url=url.split('?product_id=')[0]
        url=url.split('?src=')[0]
        try:
            html = requests.get(url)
        except Exception as e:
            print('Error in requesting Paytm(Spider): ' + str(e))
            return

        text = html.text
        soup = BeautifulSoup(text, 'html.parser')
        links = soup.find_all('a')

        print('.')
        for i in soup.find_all('h1'):
            if str(i) != 'None' and i.get('itemprop') == 'name':
                msg = str(i.get_text()).lower().strip()
                for j in Spider.wrong:
                    if msg.find(j) != -1:
                        print('..')
                        return

                print(thread_name + ' Paytm Found : ' + msg + '\n' + url + '\n\n')
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

        # for i in Spider.wrong:
        #     if lower.find(i) != -1:
        #         # print('1')
        #         return ''

        tuplle = urlparse(url)

        if tuplle.netloc == '':
            url = Spider.domain_name + url

        if url.find('paytmmall') == -1:
            # print('2')
            return ''

        if search_code == 0:
            # print('3')
            return url


        # print(url)

        if lower.find((Spider.query)[0]) != -1:
            # print('4')
            return url
        else:
            # print('5')
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
