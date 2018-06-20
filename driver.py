import threading
from Crawl.spider_amazon import Spider as Spider_Amazon
from Crawl.spider_flipkart import Spider as Spider_Flip
from Crawl.spider_paytm import Spider as Spider_Paytm
import time
import re
from mongo import MongoDB
import multiprocessing
import show_data


HOME_PAGE1 = 'https://paytmmall.com/mobiles-tablets-clpid-6942'
DOMAIN1 = 'https://www.paytmmall.com'

HOME_PAGE2 = 'https://www.amazon.in/mobile-phones/b/ref=nav_shopall_sbc_mobcomp_all_mobiles?ie=UTF8&node=1389401031'
DOMAIN2 = 'https://www.amazon.in'

HOME_PAGE3 = 'https://www.flipkart.com/mobile-phones-store?otracker=nmenu_sub_Electronics_0_Mobiles'
DOMAIN3 = 'https://www.flipkart.com'

NUMBER_OF_THREADS = 4


def spider(Spider,name,query):


    if name=='amazon':
        Spider_Amazon(HOME_PAGE2, DOMAIN2, query)


    elif name=='flipkart':
        Spider_Flip(HOME_PAGE3, DOMAIN3, query)


    elif name=='paytm':
        Spider_Paytm(HOME_PAGE1, DOMAIN1, query)



    thread_queue = []
    while len(Spider.search_results) == 0 and len(Spider.queue) != 0:
        for i in range(NUMBER_OF_THREADS):
            if len(Spider.queue) != 0 and len(Spider.search_results) == 0:
                url = Spider.queue.pop()
                t = threading.Thread(target=Spider.crawl_page, name='Thread {}'.format(i),
                                     args=('Thread {}'.format(i), url, 1))
                t.daemon = True
                thread_queue.append(t)
                t.start()

        for i in thread_queue:
            i.join()

        for i in range(len(thread_queue)):
            thread_queue.pop()

    if name=='amazon':
        mongoOperation(name,Spider_Amazon.mongo_export)

    elif name=='flipkart':
        mongoOperation(name,Spider_Flip.mongo_export)

    elif name=='paytm':
        mongoOperation(name,Spider_Paytm.mongo_export)








def my_process(list_of_process, query):
    process_queue = []
    q=multiprocessing.Queue()
    global start
    start=time.time()
    if __name__=='__main__':
        for i in list_of_process:
            if i == 'amazon':
                p1 = multiprocessing.Process(target=spider,args=(Spider_Amazon,'amazon',query ), name='amazon')
                process_queue.append(p1)
                p1.start()

            elif i == 'flipkart':
                p2 = multiprocessing.Process(target=spider,args=(Spider_Flip,'flipkart',query ), name='flipkart')
                process_queue.append(p2)
                p2.start()

            elif i == 'paytm':
                p3 = multiprocessing.Process(target=spider,args=(Spider_Paytm,'paytm',query ), name='paytm')
                process_queue.append(p3)
                p3.start()


        for p in process_queue:
            p.join()




def mongoOperation(i,data):
        if i == 'amazon':
            try:
                m1 = MongoDB('amazon')
                m1.insert(data)
            except Exception as e:
                print('Exception in MongoDB Amazon\n' + str(e))

        elif i == 'flipkart':
            try:
                m2 = MongoDB('flipkart')
                m2.insert(data)
            except Exception as e:
                print('Exception in MongoDB Flipkart\n' + str(e))


        elif i == 'paytm':
            try:
                m3 = MongoDB('paytm')
                m3.insert(data)
            except Exception as e:
                print('Exception in MongoDB Paytm\n' + str(e))

def printResult():

    print('*' * 40)
    print('*' * 40)

    print('Flipkart \n')
    print(Spider_Flip.search_results)
    print('\n')

    print('Amazon \n')
    print(Spider_Amazon.search_results)
    print('\n')

    print('Paytm \n')
    print(Spider_Paytm.search_results)
    print('\n')
    print(time.time() - start)




def format_query(query):
        l = []
        q = query.lower()
        query = re.sub('[-,/@()]', ' ', q)
        query = query.split()
        for i in query:
            l.append(i.strip())
        return l



def take_input():
    query = input('Enter you Query: ')
    query = format_query(query)
    call_crawler_Driver(query, 0)



def call_crawler_Driver(query, c):
    ecommerce = ['flipkart','paytm','amazon']
    result=MongoDB.getData(query)

    for i in result:
        if i['url'].find('amazon')!=-1:
            ecommerce.remove('amazon')

        elif i['url'].find('paytm')!=-1:
            ecommerce.remove('paytm')

        elif i['url'].find('flipkart')!=-1:
            ecommerce.remove('flipkart')

    print('Crawling for these e-commerce: '),
    print(ecommerce)

    if len(ecommerce) > 0 and c == 0:
        my_process(ecommerce, query)
        call_crawler_Driver(query,1)

    elif c==1 or len(ecommerce)==0:
        for i in result:
            print(i)
        show_data.show(result)


if __name__=='__main__':
    take_input()







