'''
https://presedinte.md/app/webroot/Constitutia_RM/Constitutia_RM_RO.pdf

https://www.legis.md/cautare/getResults?doc_id=121991&lang=ro

https://www.legis.md/cautare/getResults?doc_id=112573&lang=ro

https://www.legis.md/cautare/getResults?doc_id=112574&lang=ro
'''

print('Drilling...')

import requests
from bs4 import BeautifulSoup
import tqdm
from unidecode import unidecode
import re

jurnal_md_articles = open('moldova/jurnal_md_articles.txt', 'w', encoding='utf-8')
moldova1_articles = open('moldova/moldova1_articles.txt', 'w', encoding='utf-8')
realitatea_articles = open('moldova/realitatea_articles.txt', 'w', encoding='utf-8')
cotidianul_articles = open('moldova/cotidianul_articles.txt', 'w', encoding='utf-8')
vocea_basarabiei_articles = open('moldova/vocea_basarabiei_articles.txt', 'w', encoding='utf-8')
zugo_articles = open('moldova/zugo_articles.txt', 'w', encoding='utf-8')
esp_articles = open('moldova/esp_articles.txt', 'w', encoding='utf-8')
expresul_articles = open('moldova/expresul_articles.txt', 'w', encoding='utf-8')
nordnews_articles = open('moldova/nordnews_articles.txt', 'w', encoding='utf-8')
unica_articles = open('moldova/unica_articles.txt', 'w', encoding='utf-8')
noimd_articles = open('moldova/noimd_articles.txt', 'w', encoding='utf-8')
gazetadechisinau_articles = open('moldova/gazetadechisinau.txt', 'w', encoding='utf-8')
mineducatiei_articles = open('moldova/mineducatiei_articles.txt', 'w', encoding='utf-8')
zdg_articles = open('moldova/zdg_articles.txt', 'w', encoding='utf-8')

# jurnal_md_articles.write('')
# moldova1_articles.write('')
# realitatea_articles.write('')
# cotidianul_articles.write('')
# vocea_basarabiei_articles.write('')
# zugo_articles.write('')
# esp_articles.write('')
# expresul_articles.write('')
# nordnews_articles.write('')
# unica_articles.write('')

def jurnal_md():

    jurnal_md_articles.write('Jurnal.md\n\n')

    base_url = 'https://www.jurnal.md/'
    site = 'https://www.jurnal.md/ro/page/ultima-ora'

    for i in range(1, 100):
        print(base_url + ' :  ' + str(i))
        response = requests.get(site + '/' + str(i))
        all_news = BeautifulSoup(response.text, 'html.parser')
        all_news = all_news.find_all('a', class_='animsition-link')

        # Filter elements with exactly one class
        all_news_filtered = [el[ 'href' ] for el in all_news if len(el[ 'class' ]) == 1 and el[ 'href' ] != '/ro' and el[ 'href' ] != '/']

        all_news_filtered = list(set(all_news_filtered))


        for link in all_news_filtered:
            response = requests.get(base_url + link)
            soup = BeautifulSoup(response.text, 'html.parser')
            # print(soup.prettify())
            # Paste content to a text file in utf-8 format
            # with open('content.txt', 'w', encoding='utf-8') as f:
            #     f.write(soup.prettify())
            meta_data = soup.find_all('span', class_='article-meta-info')
            date = meta_data[0].text.split('/')[1].strip()
            category = meta_data[0].find('a').text
            article = soup.find('div', class_='article-content mt-3')
            title = article.find('h3').text
            paragraphs = article.find_all('p')
            text = ''
            for p in paragraphs:
                # Encode to utf-8
                text += unidecode(p.text)

            # Remove all non-letters
            text = re.sub(r'\s+', ' ', text) 
            jurnal_md_articles.write(title)
            jurnal_md_articles.write('\n')
            jurnal_md_articles.write(category)
            jurnal_md_articles.write('\n')
            jurnal_md_articles.write( ' ' + ' ' + date + '\n')
            jurnal_md_articles.write('\n')
            jurnal_md_articles.write(text + '\n')
            jurnal_md_articles.write('----------------------------------\n\n')

def moldova1():
    moldova1_articles.write('Moldova1.md\n\n')
    base_url = 'https://moldova1.md/'
    site = 'https://moldova1.md/n/ro/'
    for i in range(1, 100):
        print(base_url + ' :  ' + str(i))
        response = requests.get(site  + str(i) + '#list')
        all_news = BeautifulSoup(response.text, 'html.parser')
        # print(all_news.prettify())  
        # Find all a tags with href attribute starting with /p/
        all_news = all_news.find_all('a', href=re.compile("^/p/"))

        # Filter elements with exactly one class
        all_news_filtered = [el[ 'href' ] for el in all_news if el[ 'href' ] != '/ro' and el[ 'href' ] != '/']

        all_news_filtered = list(set(all_news_filtered))


        for link in all_news_filtered:
            response = requests.get(base_url + link)
            soup = BeautifulSoup(response.text, 'html.parser')
            # print(soup.prettify())
            # Paste content to a text file in utf-8 format
            # with open('content.txt', 'w', encoding='utf-8') as f:
            #     f.write(soup.prettify())
            time = soup.find('time').text
            category = soup.find('a', class_='py-4 hover:underline').text
            article = soup.find('article')
            title = article.find('h2').text
            paragraphs = article.find_all('p')
            text = ''
            for p in paragraphs:
                # Encode to utf-8
                text += unidecode(p.text)

            # Remove all non-letters
            text = re.sub(r'\s+', ' ', text) 

            moldova1_articles.write(title + '\n' + category + '\n' + time)
            moldova1_articles.write('\n')
            moldova1_articles.write(text + '\n')
            moldova1_articles.write('----------------------------------\n\n')

def realitatea():

    realitatea_articles.write('Realitatea.md\n\n')

    base_url = 'https://realitatea.md/'
    site = 'https://realitatea.md/toate-stirile/page/'

    for i in range(1, 100):
        print(base_url + ' :  ' + str(i))
        response = requests.get(site + str(i))
        all_news = BeautifulSoup(response.text, 'html.parser')
        # print(all_news.prettify())  
        # Find all a tags with href attribute starting with /p/
        all_news = all_news.find_all('a', class_ = 'big-article', href=re.compile("^https://realitatea.md/"))

        # Filter elements with exactly one class
        all_news_filtered = [el[ 'href' ] for el in all_news if el[ 'href' ] != '/ro' and el[ 'href' ] != '/']

        all_news_filtered = list(set(all_news_filtered))


        for link in all_news_filtered:
            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'html.parser')
            # print(soup.prettify())
            # Paste content to a text file in utf-8 format
            # with open('content.txt', 'w', encoding='utf-8') as f:
            #     f.write(soup.prettify())
            time = soup.find('div', class_='date-time').text.strip()
            category = soup.find('span', class_='author-display-name').find('a').text.strip()
            article = soup.find('div', class_='article-container')
            title = article.find('h1').text
            paragraphs = article.find_all('p')
            text = ''
            for p in paragraphs:
                # Encode to utf-8
                text += unidecode(p.text)

            # Remove all non-letters
            text = re.sub(r'\s+', ' ', text) 
            # Write title in a big font
            realitatea_articles.write(title)
            realitatea_articles.write('\n')
            realitatea_articles.write(category + '\n' + time + ' ')
            realitatea_articles.write('\n')
            realitatea_articles.write(text + '\n')
            realitatea_articles.write('----------------------------------\n\n')

def cotidianul():
    cotidianul_articles.write('Cotidianul.md\n\n')

    base_url = 'https://cotidianul.md/'
    site = 'https://cotidianul.md/category/actualitate/page/'

    for i in range(1, 100):
        print(base_url + ' :  ' + str(i))
        response = requests.get(site + str(i) + '/')
        all_news = BeautifulSoup(response.text, 'html.parser')
        # print(all_news.prettify())  
        # Find all a tags with href attribute starting with /p/
        articles = all_news.find_all('article')
        all_news = []
        for article in articles:
            all_news.append(article.find('a', href=re.compile("^https://cotidianul.md/")))

        # Filter elements with exactly one class
        all_news_filtered = [el[ 'href' ] for el in all_news if el[ 'href' ] != '/ro' and el[ 'href' ] != '/']

        all_news_filtered = list(set(all_news_filtered))


        for link in all_news_filtered[1:]:
            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'html.parser')
            # print(soup.prettify())
            # Paste content to a text file in utf-8 format
            # with open('content.txt', 'w', encoding='utf-8') as f:
            #     f.write(soup.prettify())
            
            category = soup.find('div', class_='meta f-meta my-3').find('span', class_ = 'cat').text .strip()
            category = re.search(r'\\ (.*) \\', category).group(1)
            time = soup.find('div', class_='meta f-meta my-3').find('span', class_ = 'date').text.strip()
            title = soup.find('header', class_='dropcap')
            title = title.find('h1').text
            article = soup.find('div', class_='content')
            paragraphs = article.find_all('p')
            text = ''
            for p in paragraphs:
                # Encode to utf-8
                text += unidecode(p.text)

            # Remove all non-letters
            text = re.sub(r'\s+', ' ', text) 
            cotidianul_articles.write(title)
            cotidianul_articles.write('\n')
            cotidianul_articles.write(category + '\n' + time + ' ' + ' ')
            cotidianul_articles.write('\n')
            cotidianul_articles.write(text + '\n')
            cotidianul_articles.write('----------------------------------\n\n')

def vocea_basarabiei():
    vocea_basarabiei_articles.write('Vocea Basarabiei\n\n')

    base_url = 'https://voceabasarabiei.md'
    site = 'https://voceabasarabiei.md/category/politic/page/'

    for i in range(1, 100):
        print(base_url + ' :  ' + str(i))
        response = requests.get(site + str(i) + '/')
        all_news = BeautifulSoup(response.text, 'html.parser')
        # print(all_news.prettify())  
        # Find all a tags with href attribute starting with /p/
        articles = all_news.find_all('p', class_='entry-title')
        all_news = []
        for article in articles:
            all_news.append(article.find('a', href=re.compile("^https://voceabasarabiei.md/")))

        # Filter elements with exactly one class
        all_news_filtered = [el[ 'href' ] for el in all_news if el[ 'href' ] != '/ro' and el[ 'href' ] != '/']

        all_news_filtered = list(set(all_news_filtered))


        for link in all_news_filtered:
            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'html.parser')
            # print(soup.prettify())
            # Paste content to a text file in utf-8 format
            # with open('content.txt', 'w', encoding='utf-8') as f:
            #     f.write(soup.prettify())
            time = soup.find('time').text.strip()
            category = 'politic'
            title = soup.find('h1', class_='tdb-title-text').text
            article = soup.find('div', class_='td_block_wrap tdb_single_content tdi_79 td-pb-border-top td_block_template_1 td-post-content tagdiv-type')
            paragraphs = article.find_all('p')
            text = ''
            for p in paragraphs:
                # Encode to utf-8
                if p.class_ != 'multiple-authors-description' or p.class_ != 'multiple-authors-links':
                    text += unidecode(p.text)

            # Remove all non-letters
            text = re.sub(r'\s+', ' ', text) 
            vocea_basarabiei_articles.write(title)
            vocea_basarabiei_articles.write('\n')
            vocea_basarabiei_articles.write(category + '\n' + time + ' ' + ' ')
            vocea_basarabiei_articles.write('\n')
            vocea_basarabiei_articles.write(text + '\n')
            vocea_basarabiei_articles.write('----------------------------------\n\n')

def zugo():
    zugo_articles.write('Zugo.md\n\n')

    base_url = 'https://zugo.md/'
    site = 'https://zugo.md/category/toate-stirile/page/'

    for i in range(1, 500):
        print(base_url + ' :  ' + str(i))
        response = requests.get(site + '/' + str(i))
        all_news = BeautifulSoup(response.text, 'html.parser')
        articles = all_news.find_all('h2', class_='post-title')
        all_news = []
        for article in articles:
            all_news.append(article.find('a', href=re.compile("^https://zugo.md/")))


        # Filter elements with exactly one class
        all_news_filtered = [el[ 'href' ] for el in all_news if el[ 'href' ] != '/ro' and el[ 'href' ] != '/']

        all_news_filtered = list(set(all_news_filtered))


        for link in all_news_filtered:
            response = requests.get(base_url + link)
            soup = BeautifulSoup(response.text, 'html.parser')
            # print(soup.prettify())
            # Paste content to a text file in utf-8 format
            # with open('content.txt', 'w', encoding='utf-8') as f:
            #     f.write(soup.prettify())
            time = soup.find('div', id='single-post-meta').find('span', class_='date').text.strip()
            category = soup.find('div', class_='category_name').find('a').text.strip()
            article = soup.find('article', id='the-post')
            title = article.find('h1').text
            paragraphs = article.find_all('p')
            text = ''
            for p in paragraphs:
                # Encode to utf-8
                text += unidecode(p.text)

            # Remove all non-letters
            text = re.sub(r'\s+', ' ', text) 

                # Write title in a big font
            zugo_articles.write(title)
            zugo_articles.write('\n')
            zugo_articles.write(category + '\n' + time + ' ' + ' ')
            zugo_articles.write('\n')
            zugo_articles.write(text + '\n')
            zugo_articles.write('----------------------------------\n\n')


def esp():
    esp_articles.write('Esp.md\n\n')

    base_url = 'https://esp.md/'
    site = 'https://esp.md/ro/podrobnosti?page='

    for i in range(1, 100):
        print(base_url + ' :  ' + str(i))
        response = requests.get(site + str(i - 1))
        all_news = BeautifulSoup(response.text, 'html.parser')
        articles = all_news.find_all('h2')
        all_news = []
        for article in articles:
            all_news.append(article.find('a', href=re.compile("^/ro/podrobnosti/")))

        # Filter elements with exactly one class
        all_news_filtered = [el[ 'href' ] for el in all_news if el != None and el[ 'href' ] != '/ro' and el[ 'href' ] != '/']

        all_news_filtered = list(set(all_news_filtered))

        # print(all_news_filtered)
        for link in all_news_filtered:
            response = requests.get(base_url + link)
            soup = BeautifulSoup(response.text, 'html.parser')
            # print(soup.prettify())
            # Paste content to a text file in utf-8 format
            # with open('content.txt', 'w', encoding='utf-8') as f:
            #     f.write(soup.prettify())
            time = soup.find('div', class_='group-header').find('div', class_='field-item even').text.strip()
            category = soup.find('div', class_='group-header').find('li', class_='field-item even')
            if category != None:
                category = category.text.strip()
            article = soup.find('div', role='article')
            title = article.find('h1').text
            paragraphs = article.find_all('p')
            text = ''
            for p in paragraphs:
                # Encode to utf-8
                text += unidecode(p.text)

            # Remove all non-letters
            text = re.sub(r'\s+', ' ', text) 

                # Write title in a big font
            esp_articles.write(title)
            esp_articles.write('\n')
            if category != None:
                esp_articles.write(category + '\n')
            esp_articles.write(time + ' ' )
            esp_articles.write('\n')
            esp_articles.write(text + '\n')
            esp_articles.write('----------------------------------\n\n')

def expresul():
    expresul_articles.write('Expresul.md\n\n')

    base_url = 'https://expresul.md/'
    site = 'https://expresul.md/category/ungheni-stiri/page/'

    for i in range(1, 100):
        print(base_url + ' :  ' + str(i))
        response = requests.get(site + str(i) + '/')
        all_news = BeautifulSoup(response.text, 'html.parser')
        articles = all_news.find_all('h3', class_='entry-title')
        all_news = []
        for article in articles:
            all_news.append(article.find('a', href=re.compile("^https://expresul.md/")))

        # Filter elements with exactly one class
        all_news_filtered = [el[ 'href' ] for el in all_news if el != None and el[ 'href' ] != '/ro' and el[ 'href' ] != '/']

        all_news_filtered = list(set(all_news_filtered))


        for link in all_news_filtered:
            response = requests.get(base_url + link)
            soup = BeautifulSoup(response.text, 'html.parser')
            # print(soup.prettify())
            # Paste content to a text file in utf-8 format
            # with open('content.txt', 'w', encoding='utf-8') as f:
            #     f.write(soup.prettify())
            time = soup.find('time').text.strip()
            category = soup.find('span', class_='article-categories').find('a').text.strip()
            article = soup.find('div', class_='neno-article-wrapper')
            title = article.find('h1').text
            paragraphs = article.find_all('p')
            text = ''
            for p in paragraphs:
                # Encode to utf-8
                text += unidecode(p.text)

            # Remove all non-letters
            text = re.sub(r'\s+', ' ', text) 

                # Write title in a big font
            expresul_articles.write(title)
            expresul_articles.write('\n')
            expresul_articles.write(category + '\n' + time)
            expresul_articles.write('\n')
            expresul_articles.write(text + '\n')
            expresul_articles.write('----------------------------------\n\n')

def nordnews():
    nordnews_articles.write('Nordnews.md\n\n')

    base_url = 'https://nordnews.md/'
    site = 'https://nordnews.md/category/social/page/'

    for i in range(1, 100):
        print(base_url + ' :  ' + str(i))
        response = requests.get(site + str(i) + '/')
        all_news = BeautifulSoup(response.text, 'html.parser')
        articles = all_news.find_all('h2', class_='title')
        all_news = []
        for article in articles:
            all_news.append(article.find('a', href=re.compile("^https://nordnews.md/")))

        # Filter elements with exactly one class
        all_news_filtered = [el[ 'href' ] for el in all_news if el != None and el[ 'href' ] != '/ro' and el[ 'href' ] != '/']

        all_news_filtered = list(set(all_news_filtered))


        for link in all_news_filtered:
            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'html.parser')
            # print(soup.prettify())
            # Paste content to a text file in utf-8 format
            # with open('content.txt', 'w', encoding='utf-8') as f:
            #     f.write(soup.prettify())
            category = 'social'
            time = soup.find('time').find('b').text.strip()
            article = soup.find('article')
            paragraphs = article.find_all('p')
            title = soup.find('span', class_='post-title').text.strip()
            text = ''
            for p in paragraphs:
                # Encode to utf-8
                text += unidecode(p.text)

            # Remove all non-letters
            text = re.sub(r'\s+', ' ', text) 


            nordnews_articles.write(title)
            nordnews_articles.write('\n')
            nordnews_articles.write(category + '\n' + time + ' ')
            nordnews_articles.write('\n')
            nordnews_articles.write(text + '\n')
            nordnews_articles.write('----------------------------------\n\n')
        

def unica():
    unica_articles.write('Unica.md\n\n')

    base_url = 'https://unica.md/'
    site = 'https://unica.md/sport/page/'

    for i in range(1, 100):
        print(base_url + ' :  ' + str(i))
        response = requests.get(site + str(i) + '/')
        all_news = BeautifulSoup(response.text, 'html.parser')
        articles = all_news.find_all('article', class_='article article-vm-teaser')
        all_news = []
        for article in articles:
            all_news.append(article.find('a', href=re.compile("^https://unica.md/")))

        # Filter elements with exactly one class
        all_news_filtered = [el[ 'href' ] for el in all_news if el != None and el[ 'href' ] != '/ro' and el[ 'href' ] != '/']

        all_news_filtered = list(set(all_news_filtered))


        for link in all_news_filtered:
            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'html.parser')
            # print(soup.prettify())
            # Paste content to a text file in utf-8 format
            # with open('content.txt', 'w', encoding='utf-8') as f:
            #     f.write(soup.prettify())

            article = soup.find('article')
            title = article.find('h1').text
            time = soup.find('div', class_='article-date').text.strip()
            category = 'sport'
            paragraphs = article.find_all('p')
            text = ''
            for p in paragraphs:
                # Encode to utf-8
                text += unidecode(p.text)

            # Remove all non-letters
            text = re.sub(r'\s+', ' ', text) 

            # Write title in a big font
            unica_articles.write(title)
            unica_articles.write('\n')
            unica_articles.write(category + '\n' + time + ' ')
            unica_articles.write('\n')
            unica_articles.write(text + '\n')
            unica_articles.write('----------------------------------\n\n')

# ## # New websites added after the first presentation

def noimd():
    noimd_articles.write('Noi.md\n\n')

    base_url = 'https://noi.md'
    site = 'https://noi.md/md/news/topread/?p=4&page='

    for i in range(1, 100):
        response = requests.get(site + str(i) + '/')
        all_news = BeautifulSoup(response.text, 'html.parser')
        articles = all_news.find_all('div', class_='col-6 pl-1 pr-1 wrp')
        # print(articles)
        all_news = []
        for article in articles:
            all_news.append(article.find('a', href=re.compile("^/md/")))

        # Filter elements with exactly one class
        all_news_filtered = [el[ 'href' ] for el in all_news if el != None and el[ 'href' ] != '/ro' and el[ 'href' ] != '/']

        all_news_filtered = list(set(all_news_filtered))


        for link in all_news_filtered:
            response = requests.get(base_url + link)
            soup = BeautifulSoup(response.text, 'html.parser')
            # print(soup.prettify())
            # Paste content to a text file in utf-8 format
            # with open('content.txt', 'w', encoding='utf-8') as f:
            #     f.write(soup.prettify())

            article = soup.find('div', class_='row news-text')
            title = soup.find('div', class_='col-12 col-lg-8 col-xl-6 news-block').find('div', class_='col-12').find('h1').text
            time = soup.find('div', class_='date-news-bar').text.strip()
            category = soup.find('div', class_='date-news-bar').find('a').text
            paragraphs = article.find_all('p')
            text = ''
            for p in paragraphs:
                # Encode to utf-8
                text += unidecode(p.text)

            # Remove all non-letters
            text = re.sub(r'\s+', ' ', text) 

            # Write title in a big font
            noimd_articles.write(title)
            noimd_articles.write('\n')
            noimd_articles.write(category + '\n' + time + ' ')
            noimd_articles.write('\n')
            noimd_articles.write(text + '\n')
            noimd_articles.write('----------------------------------\n\n')

def gazetadechisinau():
    gazetadechisinau_articles.write('gazetadechisinau.md\n\n')

    base_url = 'https://gazetadechisinau.md/'
    site1 = 'https://gazetadechisinau.md/category/stiri/page/'
    site2 = 'https://gazetadechisinau.md/category/politica/page/'
    site3 = 'https://gazetadechisinau.md/category/economie/page/'
    site4 = 'https://gazetadechisinau.md/category/sport/page/'
    site5 = 'https://gazetadechisinau.md/category/cultura/page/'
    site6 = 'https://gazetadechisinau.md/category/societate/page/'

    sites = [site1, site2, site3, site4, site5, site6]

    for site in sites:
        print(site)
        for i in range(1, 100):
            print(base_url + ' :  ' + str(i))
            response = requests.get(site + str(i) + '/')
            all_news = BeautifulSoup(response.text, 'html.parser')
            articles = all_news.find_all('h3', class_='entry-title td-module-title')
            all_news = []
            for article in articles:
                all_news.append(article.find('a', href=re.compile("^https://gazetadechisinau.md/")))

            # Filter elements with exactly one class
            all_news_filtered = [el[ 'href' ] for el in all_news if el != None and el[ 'href' ] != '/ro' and el[ 'href' ] != '/']

            all_news_filtered = list(set(all_news_filtered))


            for link in all_news_filtered:
                response = requests.get(link)
                soup = BeautifulSoup(response.text, 'html.parser')
                # print(soup.prettify())
                # Paste content to a text file in utf-8 format
                # with open('content.txt', 'w', encoding='utf-8') as f:
                #     f.write(soup.prettify())

                article = soup.find('div', class_='td-post-content td-pb-padding-side')
                title = soup.find('div', class_='td-post-header td-pb-padding-side').find('h1').text
                time = soup.find('time', class_='entry-date updated td-module-date').text.strip()
                category = soup.find('ul', class_='td-category').find('a').text
                paragraphs = article.find_all('p')
                text = ''
                for p in paragraphs:
                    # Encode to utf-8
                    text += unidecode(p.text)

                # Remove all non-letters
                text = re.sub(r'\s+', ' ', text) 

                # Write title in a big font
                gazetadechisinau_articles.write(title)
                gazetadechisinau_articles.write('\n')
                gazetadechisinau_articles.write(category + '\n' + time + ' ')
                gazetadechisinau_articles.write('\n')
                gazetadechisinau_articles.write(text + '\n')
                gazetadechisinau_articles.write('----------------------------------\n\n')


def mineducatiei():
    mineducatiei_articles.write('www.mec.gov.md/ro\n\n')

    base_url = 'https://www.mec.gov.md/'
    site = 'https://www.mec.gov.md/ro/press-releases?page='

    for i in range(1, 100):
        print(base_url + ' :  ' + str(i))
        headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
        response = requests.get(site + str(i) + '/', headers=headers)
        all_news = BeautifulSoup(response.text, 'html.parser')
        articles = all_news.find_all('h4', class_='views-field views-field-title')
        all_news = []
        for article in articles:
            all_news.append(article.find('a', href=re.compile("^/ro/content/")))

        # Filter elements with exactly one class
        all_news_filtered = [el[ 'href' ] for el in all_news if el != None and el[ 'href' ] != '/ro' and el[ 'href' ] != '/']

        all_news_filtered = list(set(all_news_filtered))


        for link in all_news_filtered:
            response = requests.get(base_url + link, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            # print(soup.prettify())
            # Paste content to a text file in utf-8 format
            # with open('content.txt', 'w', encoding='utf-8') as f:
            #     f.write(soup.prettify())

            article = soup.find('div', class_='panel-panel panel-col')
            title = article.find('div', class_='panel-pane pane-token pane-node-title pane-title').find('div', class_='pane-content').text.strip()
            time = soup.find('div', class_='panel-pane pane-node-created').find('div', class_='pane-content').text.strip()
            category = 'educatie'
            paragraphs = article.find_all('span')
            text = ''
            for p in paragraphs:
                # Encode to utf-8
                text += unidecode(p.text)

            # Remove all non-letters
            text = re.sub(r'\s+', ' ', text) 

            # Write title in a big font
            mineducatiei_articles.write(title)
            mineducatiei_articles.write('\n')
            mineducatiei_articles.write(category + '\n' + time + ' ')
            mineducatiei_articles.write('\n')
            mineducatiei_articles.write(text + '\n')
            mineducatiei_articles.write('----------------------------------\n\n')


# jurnal_md()
# moldova1()
# realitatea()
# cotidianul()
# vocea_basarabiei()
# zugo()
# esp()
# expresul()
# nordnews()
# unica()
# noimd()
# gazetadechisinau()
# mineducatiei()
# Create a thread for each function
import threading
threading.Thread(target=jurnal_md).start()
threading.Thread(target=moldova1).start()
threading.Thread(target=realitatea).start()
# threading.Thread(target=cotidianul).start()
threading.Thread(target=vocea_basarabiei).start()
threading.Thread(target=zugo).start()
threading.Thread(target=esp).start()
threading.Thread(target=expresul).start()
threading.Thread(target=nordnews).start()
threading.Thread(target=unica).start()
threading.Thread(target=noimd).start()
threading.Thread(target=gazetadechisinau).start()
threading.Thread(target=mineducatiei).start()

# Wait for all threads to finish
threading.Event().wait()

# jurnal_md()

# Print in red ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print('\033[91m' + '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('\033[91m' + '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('\033[91m' + '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('\033[91m' + '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('\033[91m' + '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('\033[91m' + '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('\033[91m' + 'REACHED THE CORE. DRILLING COMPLETE.')
print('\033[91m' + '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('\033[91m' + '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('\033[91m' + '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('\033[91m' + '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('\033[91m' + '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('\033[91m' + '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
# Get back to normal
print('\033[0m')

jurnal_md_articles.close()
moldova1_articles.close()
realitatea_articles.close()
cotidianul_articles.close()
vocea_basarabiei_articles.close()
zugo_articles.close()
esp_articles.close()
expresul_articles.close()
nordnews_articles.close()
unica_articles.close()
