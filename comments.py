import chime
from datetime import date
from hepsi import *
from progress.bar import Bar
from time import sleep

"""Comment Collector.
Collects comments for given product urls in product_list.txt, 
comments are filtered by stars 1,2 and 4,5."""


chime.theme('pokemon')
td = date.today()


products_arr = []
with open('product_list.txt') as products:
    for line in products:
        products_arr.append(line.replace('\n',''))


# To collect more comments, I filtered comments  as 1,2 and 4,5.
n_comment = []
n_seller = []
n_rate = []
n_date = []
with Bar('Negative comments are loading',max=len(products_arr)) as bar:
    for product in products_arr:
        reviews = collect_reviews(product_url=product,filter='1,2')
        n_comment += reviews[0]
        n_rate += reviews[1]
        n_seller += reviews[2]
        n_date += reviews[3]
        bar.next()
df = pd.DataFrame({'Comment':n_comment, 'Rate':n_rate, 'Seller':n_seller, 'Date':n_date})
df.to_pickle(f'raw_negative{td}.pkl')
chime.success()

p_comment = []
p_seller = []
p_rate = []
p_date = []
with Bar('Positive comments are loading',max=len(products_arr)) as bar:
    for product in products_arr:
        reviews = collect_reviews(product_url=product,filter='4,5')
        p_comment += reviews[0]
        p_rate += reviews[1]
        p_seller += reviews[2]
        p_date += reviews[3]
        bar.next()
df_p = pd.DataFrame({'Comment':p_comment, 'Rate':p_rate, 'Seller':p_seller, 'Date':p_date})
df_p.to_pickle(f'raw_positive{td}.pkl')
chime.success()

