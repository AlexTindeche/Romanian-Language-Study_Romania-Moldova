import requests
from bs4 import BeautifulSoup
from time import sleep
from unidecode import unidecode


site = 'https://www.libertatea.ro/stiri'
site_2 = 'https://www.libertatea.ro/stiri/page/'
website_file = 'libertatea.txt'
links_file = 'libertatea_links.txt'
failed_links_file = 'liberatea_failed_links.txt'

first_page = requests.get(site)
soup = BeautifulSoup(first_page.content, 'html.parser')

titles = soup.find_all('h2', class_='article-title')

# links = []

# for title in titles:
#     link = title.find('a')
#     links.append(link['href'])


# for i in range(2, 3):
#     sleep(2)
#     print(f"Getting links from page {i}...")
#     page = requests.get(site_2 + str(i))
#     soup = BeautifulSoup(page.content, 'html.parser')
#     titles = soup.find_all('h2', class_='article-title')
#     for title in titles:
#         link = title.find('a')
#         links.append(link['href'])


# with open(links_file, 'w', encoding='utf-8') as file:
#     for link in links:
#         file.write(link + '\n')
        
# print(f"Got {len(links)} links.")

# with open(links_file, 'r', encoding='utf-8') as file:
#     links = file.read().splitlines()
# print(len(links))
# # exit(0)

articles = []
with open(links_file, 'r', encoding='utf-8') as file:
    links = file.read().splitlines()
    
print(len(links))

link_no = 0
link_exception = 0
failed_links = []

with open(website_file, 'w', encoding='utf-8') as file:
    file.write('libertatea.ro\n\n')

for link in links:
    link_no += 1
    if link_no - len(failed_links) > 500:
        break
    
    if link_no % 5 == 0:
        print(f"Getting article {link_no}/{len(links)} (errors so far {link_exception}: projected {len(links) - link_exception})...")
        with open(website_file, 'a', encoding='utf-8') as file:
            for article in articles:
                file.write(article)
                
            articles = []
        sleep(2)
    
    try:
        article = requests.get(link)
        soup = BeautifulSoup(article.content, 'html.parser')
        
        art_title = soup.find('h1').text
        art_categ = soup.find('span', class_='breadcrumbs')
        art_categ = art_categ.find_all('a')
        art_categ = art_categ[-1].text
        
        art_time = soup.find('div', class_='time-content').find('span').text
        
        art_text = soup.find('p', class_='intro').text

        article = soup.find('div', class_='article-body').find('div', id='content-wrapper')
        paragraphs = article.find_all('p')
        for p in paragraphs:
                # Encode to utf-8
                art_text += unidecode(p.text)
        
        # art_text += '\n\n' + soup.find('div', class_='article-body').find('div', id='content-wrapper').text

        # print(art_text)

        # articles.append(art_title + "\n" + art_categ + "\n" + art_time + "\n" + art_text + "\n----------------------------------\n\n")
    except(Exception) as e:
        print(f"Error {link}: {e}")
        link_exception += 1
        failed_links.append(link)
        
print(f"Got {len(links) - len(failed_links)} articles.")
        
        
with open(failed_links_file, 'w', encoding='utf-8') as file:
    for link in failed_links:
        file.write(link + '\n')