import requests
from bs4 import BeautifulSoup
from time import sleep
from unidecode import unidecode


site = 'https://www.dcnews.ro/news.html'
site_2 = 'https://www.dcnews.ro/news_'
website_file = 'dcnews.txt'
links_file = 'dcnews_links.txt'
failed_links_file = 'dcnews_failed_links.txt'

# first_page = requests.get(site)
# soup = BeautifulSoup(first_page.content, 'html.parser')

# titles = soup.find_all('a', class_='box_mic_img')

# links = []

# for title in titles:
#     # link = title.find('a')
#     links.append(title['href'])
    


# for i in range(2, 3):
#     print(f"So far got {len(links)} links")
#     sleep(2)
#     print(f"Getting links from page {i}...")
#     page = requests.get(site_2 + str(i) + '.html')
#     soup = BeautifulSoup(page.content, 'html.parser')
#     titles = soup.find_all('a', class_='box_mic_img')
#     for title in titles:
#         # link = title.find('a')
#         links.append(title['href'])

# with open(links_file, 'w', encoding='utf-8') as file:
#     for link in links:
#         file.write(link + '\n')
        
# print(f"Got {len(links)} links.")


with open(links_file, 'r', encoding='utf-8') as file:
    links = file.read().splitlines()
print(len(links))

articles = []

link_no = 0
link_exception = 0
failed_links = []

with open(website_file, 'w', encoding='utf-8') as file:
    file.write('dcnews.ro\n\n')

for link in links[1:2]:
    link_no += 1
    if link_no % 5 == 0:
        print(f"Getting article {link_no}/{len(links)} (errors so far {link_exception}: projected {len(links) - link_exception})...")
        with open(website_file, 'a', encoding='utf-8') as file:
            for article in articles:
                file.write(article)
                
            articles = []
        sleep(1)
    
    try:
        article = requests.get(link)
        soup = BeautifulSoup(article.content, 'html.parser')
        
        art_title = soup.find('h1').text
        art_categ = soup.find('div', class_='breadcrumbs')
        art_categ = art_categ.find_all('a')
        art_categ = art_categ[-1].text
        
        
        art_time = soup.find('time')['datetime']

        article = soup.find('div', class_='articol_dec')
        paragraphs = article.find_all('p')
        art_text = ''
        for p in paragraphs:
                # Encode to utf-8
                art_text += unidecode(p.text)
        
        # art_text = soup.find('div', id='articleContent').text
        # print(art_title.strip())
        # print('----------------')
        # print(art_categ)
        # print('----------------')
        # print(art_text)
        
        # art_text += '\n\n' + soup.find('div', class_='article-body').find('div', id='content-wrapper').text

        articles.append(art_title + "\n" + art_categ + "\n" + art_time + "\n" + art_text + "\n----------------------------------\n\n")
    except(Exception) as e:
        print(f"Error {link}: {e}")
        link_exception += 1
        failed_links.append(link)
        
print(f"Got {len(articles)} articles.")
        
    

        
with open(failed_links_file, 'w', encoding='utf-8') as file:
    for link in failed_links:
        file.write(link + '\n')