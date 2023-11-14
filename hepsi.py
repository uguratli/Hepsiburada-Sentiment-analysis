import requests
import re
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np




def make_request(url):
    """Request maker.
    Makes request for given url."""
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    return requests.get(url=url, headers=headers)


def make_soup(url):
    """Soup maker.
    Returns soup for given url."""
    r = make_request(url)
    if r.status_code == 200:
        return bs(r.content, 'html5lib')
    else:
        return False
def get_pages(url=None, soup=None):
    """
    Returns current and total page for given product page."""
    if soup == None:
        soup = make_soup(url)
    page = soup.find('div', {'class': "paginationBarHolder"})
    if page != None:
        return [int(x) for x in re.search(r'Önceki(.*?)Sonraki', page.text).group(1).split('/')]
    else:
        return 1, 2
    
def get_seller_name(text):
    """
    Returns seller."""
    if re.search(r'Kullanıcı bu ürünü(.*?)satıcısından aldı', text) != None:
        return re.search(r'Kullanıcı bu ürünü(.*?)satıcısından aldı', text).group(1).strip()
    else:
        return None
def get_reviews1(url=None, soup=None):
    """Page reviews collector.
    Returns reviews on given page url or soup."""
    if soup == None:
        soup = make_soup(url)
    date = []
    seller = []
    rate = []
    comment = []
    if soup:
        reviews = soup.find_all('div', {'itemprop': "review"})
        for i in range(len(reviews)):
            if reviews[i].find('span', {'itemprop': 'description'}) != None:
                comment.append(reviews[i].find('span', {'itemprop': 'description'}).text)
            else:
                comment.append(np.nan)
            rate.append(reviews[i].find('span', {'itemprop': 'ratingValue'}).attrs['content'])
            seller.append(get_seller_name(reviews[i].text))
            date.append(reviews[i].find('span', {'itemprop': 'datePublished'}).attrs['content'])
        return comment, rate, seller, date
    else:
        return None
def get_reviews(url=None, soup=None):
    """Page reviews collector.
    Returns reviews on given page url or soup."""
    if soup == None:
        soup = make_soup(url)
    date = []
    seller = []
    rate = []
    comment = []
    if soup:
        reviews = soup.find_all('div', {'itemprop': "review"})
        for review in reviews:
            if review.find('span', {'itemprop': 'description'}) != None:
                comment.append(review.find('span', {'itemprop': 'description'}).text)
            else:
                comment.append(np.nan)
            rate.append(review.find('span', {'itemprop': 'ratingValue'}).attrs['content'])
            seller.append(get_seller_name(review.text))
            date.append(review .find('span', {'itemprop': 'datePublished'}).attrs['content'])
        return comment, rate, seller, date
    else:
        return None    
def collect_reviews(product_url, filter='', dataframe=False):
    """Product reviews collector.
    Takes product page url, sorts reviews according to date, can filter reviews and returns half of the total reviews,
    since hepsiburada allows us to access almost half of tatal reviews via link.
    Function retuns dataframe or array(comment, rate, seller name, review date), dataframe is False
    by default."""
    comments = []
    rates = []
    sellers = []
    dates = []
    page = 1
    url = product_url + f'-yorumlari?sayfa={page}'
    soup = make_soup(url)
    pages = get_pages(soup=soup)
    for page in range(pages[0], int((pages[1]+2)/2)):
        url = product_url + f'-yorumlari?sirala=createdAt&sayfa={page}&filtre={filter}'
        soup = make_soup(url)
        reviews = get_reviews(soup=soup)
        comments += reviews[0]
        rates += reviews[1]
        sellers += reviews[2]
        dates += reviews[3]

    if dataframe :
        return pd.DataFrame({'Coment':comments, 'Rate':rates, 'Seller':sellers, 'Date':dates})
    else:
        return comments, rates, sellers, dates
def get_product_count(url=None, soup=None):
    """
    Returns number of total products for given category and number of maximum products shown in page
    Number of product per page, total product"""
    pattern = str.maketrans('', '', '+')
    if soup == None:
        soup = make_soup(url)
    return [int(x) for x in re.search(r'Toplam(.*?) ürün', soup.text).group(1).translate(pattern).split('/')]

def get_products_url(url=None, soup=None):
    """Product url collector.
    Returns page urls of all products in given page, takes url or soup."""
    base = 'https://www.hepsiburada.com'
    if soup == None:
        soup = make_soup(url)
    products = soup.find('div', {'class': "product-list-category"}).findAll('a')
    return [base+product['href'] for product in products]

def harvest_category(url=None, soup=None, max=1, filter='', dataframe=False):
    """Reviews collector.
    Collects reviews of top reviewed products for given category page, maximum products is limited to 1 by default.
    Returns reviews as dataframe of array, dataframe is False by default."""
    comments = []
    rates = []
    sellers = []
    dates = []
    page = 1 
    #category_url = url
    category_url = url+'?siralama=yorumsayisi&sayfa={page}'
    if soup == None:
        soup = make_soup(category_url)
    product_per_page, product_total = get_product_count(soup=soup)
    if max > product_total:
        print('Max exceed total product')
        return None
    else:
        urls = get_products_url(soup=soup)
        for i in range(max):
            index = (i-(page-1)*product_per_page)
            product_reviews = collect_reviews(product_url=urls[index], filter=filter)
            comments += product_reviews[0]
            rates += product_reviews[1]
            sellers += product_reviews[2]
            dates += product_reviews[3]
            if (i+1)%product_per_page == 0:
                page += 1
                category_url = url+'?siralama=yorumsayisi&sayfa={page}'
                urls = get_products_url(url=category_url)
        if dataframe:
            return pd.DataFrame({'Comment':comments, 'Rate':rates, 'Seller':sellers, 'Date':dates})
        else:
            return comments, rates, sellers, dates
