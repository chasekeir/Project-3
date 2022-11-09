import argparse
import requests
from bs4 import BeautifulSoup
import json
import csv

def parse_itemssold(text):
    '''
    Takes as input a string and returns the number of items sold, as specified in the string.
    
    >>> parse_itemssold('38 sold')
    38
    >>> parse_itemssold('34 watchers')
    0
    >>> parse_itemssold('Almost gone')
    0
    '''
    numbers = ''
    for char in text:
        if char in '1234567890':
            numbers += char
    if 'sold' in text:
        return int(numbers)
    else:
        return 0

def parse_price(text):
    '''
    >>> parse_price('$340.55')
    34055
    >>> parse_price('$0.99 to $49.95')
    99
    >>> parse_price('Tap item to see current priceSee price')
    
    '''
    numbers = ''
    if text[0] == '$':
        for char in text:
            if char in '1234567890':
                numbers += char
            elif char == ' ':
                break
        return int(numbers)
    else:
        return None

def parse_shipping(text):
    '''
    >>> parse_price(+$8.95 shipping)
    895
    >>> parse_price(Free shipping)
    0
    '''
    numbers = ''
    if text[0] == '+':
        for char in text:
            if char in '1234567890':
                numbers += char
            elif char == ' ':
                break
        return int(numbers)
    else:
        return 0


# get command line argumants
parser = argparse.ArgumentParser(description='Download information from ebay and convert it to JSON.')
parser.add_argument('search_term')
parser.add_argument('--num_pages', default=10)
parser.add_argument('--csv', default = False)
args = parser.parse_args()
print('args.search_term=', args.search_term)

#list of all items found in all ebay web pages
items = []

#loop over the ebay webpages
for page_number in range(1,int(args.num_pages)+1):

    #build the url
    url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw='
    url += args.search_term
    url += '&_sacat=0&_pgn='
    url += str(page_number)
    url += '&rt=nc'
    print ('url=', url)

    #download the html
    r = requests.get(url)
    status = r.status_code
    print('status=', status)
    html = r.text

    #process the html
    soup = BeautifulSoup(html, 'html.parser')


    #loop over items in the page
    tags_items = soup.select('.s-item')
    for tag_item in tags_items:

#status like name
        #extract name
        name = None
        tags_name = tag_item.select('.s-item__title')
        for tag in tags_name:
            name = tag.text

        #extract status
        status = None
        tags_status = tag_item.select('.SECONDARY_INFO')
        for tag in tags_status:
            status = tag.text

        #extract free returns
        freereturns = False
        tags_freereturns = tag_item.select('.s-item__free-returns')
        for tag in tags_freereturns:
            freereturns = True

        items_sold = None
        tags_itemssold = tag_item.select('.s-item__hotness')
        for tag in tags_itemssold:
            items_sold = parse_itemssold(tag.text)

        price = None
        tags_price = tag_item.select('.s-item__price')
        for tag in tags_price:
            price = parse_price(tag.text)

        shipping = None
        tags_shipping = tag_item.select('.s-item__shipping')
        for tag in tags_shipping:
            shipping = parse_shipping(tag.text)

        item = {
            'name': name,
            'free_returns': freereturns,
            'items_sold': items_sold,
            'status': status,
            'price': price,
            'shipping': shipping
        }
        if 'Shop on eBay' in item['name']:
                continue
        else:
            items.append(item)

    print('len(tag_items)=', len(tags_items))
    print('len(items)=', len(items))


#write Json to a file
filename = args.search_term+'.json'
with open(filename, 'w', encoding='ascii') as f:
    f.write(json.dumps(items))
if args.csv: 
    keys = list(items[0].keys())
    filename_csv = args.search_term + '.csv'
    with open(filename_csv, 'w', encoding = 'utf-8', newline = '') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(items)
