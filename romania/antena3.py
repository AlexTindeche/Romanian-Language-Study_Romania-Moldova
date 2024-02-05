import requests
from bs4 import BeautifulSoup
from time import sleep


site = 'https://www.antena3.ro/stiri/'
site_2 = 'https://www.antena3.ro/stiri/pagina-'
website_file = 'antena3.txt'
links_file = 'antena3_links.txt'
failed_links_file = 'antena3_failed_links.txt'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

# first_page = requests.get(site, headers=headers)
# soup = BeautifulSoup(first_page.content, 'html.parser')

# titles = soup.find_all('article')

# links = []

# for title in titles:
#     link = title.find('h2').find('a')
#     links.append(link['href'])
    
    

# for i in range(2, 21):
#     print(f"So far got {len(links)} links")
#     sleep(2)
#     print(f"Getting links from page {i}...")
#     page = requests.get(site_2 + str(i), headers=headers)
#     soup = BeautifulSoup(page.content, 'html.parser')
#     titles = soup.find_all('article')
#     for title in titles:
#         link = title.find('h2').find('a')
#         links.append(link['href'])

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
    file.write('antena3.ro\n\n')

for link in links:
    link_no += 1
    if link_no % 5 == 0:
        print(f"Getting article {link_no}/{len(links)} (errors so far {link_exception}: projected {len(links) - link_exception})...")
        with open(website_file, 'a', encoding='utf-8') as file:
            for article in articles:
                file.write(article)
                
            articles = []
        sleep(1)
    
    try:
        article = requests.get(link, headers=headers)
        soup = BeautifulSoup(article.content, 'html.parser')
        
        art_title = soup.find('h1').text
        art_categ = soup.find('div', id='location')
        art_categ = art_categ.find_all('a')
        art_categ = art_categ[-1].text
        
        
        art_time = soup.find('div', class_="autor-ora-comentarii").find_all('span')[-1].text
        
        art_text = soup.find('div', class_='text').text
        
        # art_text += '\n\n' + soup.find('div', class_='article-body').find('div', id='content-wrapper').text

        articles.append(art_title + "\n" + art_categ + "\n" + art_time + "\n" + art_text + "\n----------------------------------\n\n")
    except(Exception) as e:
        print(f"Error {link}: {e}")
        link_exception += 1
        failed_links.append(link)
    
        
print(f"Got {len(links) - len(failed_links)} articles.")
        
with open(failed_links_file, 'w', encoding='utf-8') as file:
    for link in failed_links:
        file.write(link + '\n')