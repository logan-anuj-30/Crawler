from bs4 import BeautifulSoup
import requests


def obj(url):
    try:
        html = requests.get(url)
        h = html.text
    except Exception as e:
        print('Exception in getting data :' + str(e))
        return 'None'
    soup = BeautifulSoup(h, 'html.parser')
    return soup


def flip(soup):
    for i in soup.find_all('div'):
        a = (i.get('class'))
        if str(a) != 'None' and len(a) > 1 and str(a[0]) == '_1vC4OE' and str(a[1]) == '_3qQ9m1':
            return str(i.get_text()).strip()

# priceblock_ourprice

def amazon(soup):
    for i in soup.find_all('span'):
        if str(i)!='None' and i.get('id')=='priceblock_saleprice' or i.get('id')=='priceblock_ourprice':
            return str(i.get_text()).strip()

def paytm(soup):
    for i in soup.find_all('span'):
        if str(i.get('class')) != 'None' and (i.get('class'))[0] == '_1V3w':
            # print(i.get_text())
            return str(i.get_text()).strip()


def show(result):
    p = []
    for i in result:
        soup = obj(i['url'])#beautiful soup object
        if i['url'][12] == 'f':
            price = flip(soup)
            p.append({'site': 'flipkart', 'model': i['name'], 'url': i['url'], 'price': price})


        elif i['url'][12]=='a':
            price = amazon(soup)
            p.append({'site': 'amazon', 'model': i['name'], 'url': i['url'], 'price': price})


        elif i['url'].find('paytmmall') != -1:
            price = paytm(soup)
            p.append({'site': 'paytm', 'model': i['name'], 'url': i['url'], 'price': price})

    print('*'*30)

    for i in p:
        print('Site : ' + i['site'])
        print('Price : ' + str(i['price']))
        print('Model : ',end='')
        for j in i['model']:
            print(j+' ',end='')
        print('')
        print('URL : ' + i['url'])
        print('\n')
