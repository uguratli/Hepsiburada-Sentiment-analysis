# Sentiment Analysis on Hepsiburada

 Sentiment Analysis for TWS Headphones from Hepsiburada reviews. Procusts used for this work are listes in file named product_list.txt, dataset contains almost half of reviews of product and filtered by 1-2 and 4-5 stars to get maximun reviews. I can not share the dataset because I do not have the copyright, but I share the code that I used to collect reviews.

## Dataset Information

The dataset is made of two parts, negative reviews and positive review. Total data sets contains 103702 reviews in form of comment, rate, seller name and date where comment is comment given by user, rate is star counts can be either 1-2 (negative) and 4-5 (positive),
seller name is the name of shop that user chose for shopping, and date is day of deal. Whole columns are in type of object, and there are missing comments.

## Requirements

The libraries I used for this project are as fallows.

* `beautifulsoup4`
* `chime`
* `nltk`
* `numpy`
* `pandas`
* `progress`
* `Requests`
* `snowballstemmer`
* `time`

The libraries for trainings are:

* `sklearn`
* `sklearn-optimize`

## Usage

* `nlp_hepsiburada.ipynb` is python notebook of this project, includes preprocessing and training. For training, includes four ML algorithms ; SVM, Naive Bayes, Logistic regression, Decision tree. I made DL models too, but this one does not include them, I will add them later.
* `preprocess.py` is preprocess code, includes functions for text preprocessing.
* `hepsi.py` is review collecting code, can not work alone, includes bs4 funcions for collecting reviews from Hepsiburada.com, works for category and product. `hepsi.py` can collect almost half of total reviews, I limited for half because I cant reach all pages via url, after some point url retuns just first page and no need to waste time to collect same reviews again and again.
* `comments.py` is review collecting main code, reads product_list.txt and collect reviews (almost half) for given products. `comments.py` works alone.

## Other files

`requirements.txt`: List of libraries I used for this project.
`product_list.txt`: List of product I chose to use for this project.
`req.py`: List of imported libraries.

