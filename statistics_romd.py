import glob
import os
import numpy as np
import re

# Print current folder
print(os.getcwd())


# Read the files from Moldova folder
def read_files(folder_name):
    os.chdir(folder_name)
    files = []
    for file in glob.glob("*.txt"):
        files.append(file)
    os.chdir("..")
    return files

moldova = read_files("moldova")
romania = read_files("romania")

def get_no_of_articles(folder, files):
    no_of_articles = 0
    for file in files:
        with open(f"{folder}/" + file, "rb") as f:
            articles = f.read().decode("utf-8").split('----------------------------------')
            for article in articles:
                if article != '':
                    no_of_articles += 1
    return no_of_articles

print(get_no_of_articles("romania", romania))
print(get_no_of_articles("moldova", moldova))

def get_word_statistics(folder, files):
    word_array = []
    for file in files:
        with open(f"{folder}/" + file, "rb") as f:
            words = f.read().decode("utf-8").split()
            for word in words:
                word_array.append(len(word))
    word_array = np.array(word_array)
    return [np.mean(word_array), np.median(word_array), np.std(word_array)]

# mean_moldova, median_moldova, std_moldova = get_word_statistics("moldova", moldova)
# mean_romania, median_romania, std_romania = get_word_statistics("romania", romania)

# print(f"Mean for Moldova: {mean_moldova}")
# print(f"Median for Moldova: {median_moldova}")
# print(f"Standard deviation for Moldova: {std_moldova}")
# print(f"Mean for Romania: {mean_romania}")
# print(f"Median for Romania: {median_romania}")
# print(f"Standard deviation for Romania: {std_romania}")


def get_categories_romania(files = romania):
    categories = set()
    for file in files:
        with open(f"romania/" + file, "rb") as f:
            articles = f.read().decode("utf-8").split('----------------------------------')
            for article in articles:
                if article != '':
                    categ = re.search(r'\n*.*\n*(.*)\n*', article).group(1)
                    if len(categ.split()) <= 15 and len(categ.strip()) > 0:
                        categories.add(categ)
    return categories

def get_categories_moldova(files = moldova):
    categories = set()
    for file in files:
        if file != 'cotidianul_articles.txt':
            with open(f"moldova/" + file, "rb") as f:
                articles = f.read().decode("utf-8").split('----------------------------------')
                for article in articles:
                    if article != '':
                        categ = article.split('\n')[3]
                        if len(categ.split()) <= 10 and len(categ.strip()) > 0:
                            categories.add(categ[:-1])
    return categories


categories_romania = get_categories_romania()
categories_moldova = get_categories_moldova()

print("Number of categories in Romania: ", len(categories_romania))
print("Number of categories in Moldova: ", len(categories_moldova))

# Dictionaries for categories with articles
articles_by_category_romania = {}
articles_by_category_moldova = {}

def get_articles_by_category_romania():
    global romania, articles_by_category_romania
    for file in romania:
        with open(f"romania/" + file, "rb") as f:
            articles = f.read().decode("utf-8").split('----------------------------------')
            for article in articles:
                if article != '':
                    categ = re.search(r'\n*.*\n*(.*)\n*', article).group(1)
                    if len(categ.split()) <= 15 and len(categ.strip()) > 0:
                        categ = categ.strip()
                        if categ in ['Politic', 'politică', 'Politica', 'Politică', 'Stiri Politice Interne si Internationale', 'politic-extern',
                                            'politic-intern', 'Politica interna', 'Politica externa', 'Politica internă', 'Politica externă',
                                            'Opinie și promovare politică']:
                            if 'Politica' in articles_by_category_romania.keys():
                                articles_by_category_romania['Politica'].append(article)
                            else:
                                articles_by_category_romania['Politica'] = [article]
                        if categ in ['Economic', 'economic', 'Economie', 'economie', 'Economia', 'economia', 'Economie si Afaceri',
                                            'Stiri Economice si Financiare','Companii', 'Bani și Afaceri','Business', 'Monitorizare Europarlamentare',
                                            'Parlamentul European']:
                            if 'Economie' in articles_by_category_romania.keys():
                                articles_by_category_romania['Economie'].append(article)
                            else:
                                articles_by_category_romania['Economie'] = [article]
                        if categ in ['Social', 'social', 'Societate', 'societate', 'Societatea', 'societatea', 'Societate si Cultura',
                                            'Stiri Sociale si Culturale', 'Stiri Sociale', 'social/sanatate']:
                            if 'Social' in articles_by_category_romania.keys():
                                articles_by_category_romania['Social'].append(article)
                            else:
                                articles_by_category_romania['Social'] = [article]
                        if categ in ['Sport', 'sport', 'Sporturi', 'sporturi', 'Sporturi si Turism', 'sporturi-turism', 'Stiri din Sport ',
                                            'Fotbal intern', 'Fotbal extern',]:
                            if 'Sport' in articles_by_category_romania.keys():
                                articles_by_category_romania['Sport'].append(article)
                            else:
                                articles_by_category_romania['Sport'] = [article]
                        if categ in ['Cultura', 'cultura', 'Cultură', 'cultură', 'Cultura si Stiinta', 'cultura-stiinta', 'Stiri Culturale',
                                            'cultura-media']:
                            if 'Cultura' in articles_by_category_romania.keys():
                                articles_by_category_romania['Cultura'].append(article)
                            else:
                                articles_by_category_romania['Cultura'] = [article]
                        if categ in ['Stiri Actuale', 'Actualitate', 'Stiri', 'Stiri Externe | Stiri Internationale', 'Ultimele Stiri',
                                            'International News','Știri Externe', 'News Hour with CNN', 'Știri România', 'Război în Israel',
                                            'Știri externe', 'Ştiri', 'Știri', 'externe', 'Externe', ]:
                            if 'Stiri' in articles_by_category_romania.keys():
                                articles_by_category_romania['Stiri'].append(article)
                            else:
                                articles_by_category_romania['Stiri'] = [article]
                        if categ in ['Divertisment', 'divertisment', 'Divertisment si Utile', 'divertisment-utile', 'Stiri din Divertisment',
                                            'divertisment-media', 'Altceva Podcast', 'Film', 'entertainment', 'Mallcast', 'Muzică', 'Showbiz', 'Timp liber', 
                                            'Show', 'Vedete', 'Cancan', 'Life Show', 'eveniment']:
                            if 'Divertisment' in articles_by_category_romania.keys():
                                articles_by_category_romania['Divertisment'].append(article)
                            else:
                                articles_by_category_romania['Divertisment'] = [article]
                        if categ in ['Tehnologie', 'tehnologie', 'Tehnologie si Stiinta', 'tehnologie-stiinta', 'Stiri Tehnologie si Stiinta',
                                            'tehnologie-media', 'Știinţă', 'High Tech', 'Auto / Tech', 'România Inteligentă', 'Sci-tech', 'Stiri Stiinta si Tehnologie', 'Tehnologie']:
                            if 'Tehnologie' in articles_by_category_romania.keys():
                                articles_by_category_romania['Tehnologie'].append(article)
                            else:
                                articles_by_category_romania['Tehnologie'] = [article]
                        if categ in ['Sanatate', 'sanatate', 'Sănătate', 'sănătate', 'Sanatate si Familie', 'sanatate-familie', 'Stiri Sanatate si Familie',
                                            'sanatate-media', 'Stiri Sanatate', 'sanatate-media', 'Sănătate', 'Health','Stiri Sanatate',  'Sfat de sănătate']:
                            if 'Sanatate' in articles_by_category_romania.keys():
                                articles_by_category_romania['Sanatate'].append(article)
                            else:
                                articles_by_category_romania['Sanatate'] = [article]
                        if categ in ['Auto', 'auto', 'Auto-Moto', 'auto-moto', 'Auto si Moto', 'auto-moto', 'Stiri Auto si Moto', 'auto-media', 'STOP TRAFIC', 
                                            'Transporturi']:
                            if 'Auto' in articles_by_category_romania.keys():
                                articles_by_category_romania['Auto'].append(article)
                            else:
                                articles_by_category_romania['Auto'] = [article]
                        if categ in ['Turism', 'turism', 'Turism si Vacante', 'turism-vacante', 'Stiri Turism si Vacante', 'turism-media', 'Turism si Vacante',
                                        'Travel']:
                            if 'Turism' in articles_by_category_romania.keys():
                                articles_by_category_romania['Turism'].append(article)
                            else:
                                articles_by_category_romania['Turism'] = [article]
                        if categ in ['Lifestyle', 'lifestyle', 'Lifestyle si Utile', 'lifestyle-utile', 'Stiri Lifestyle si Utile', 'lifestyle-media', 'Lifestyle',
                                            'Life',  'Stil de viață', 'Stiri Lifestyle']:
                            if 'Lifestyle' in articles_by_category_romania.keys():
                                articles_by_category_romania['Lifestyle'].append(article)
                            else:
                                articles_by_category_romania['Lifestyle'] = [article]
                        if categ in ['Educatie', 'educatie', 'Educatie si Stiinta', 'educatie-stiinta', 'Stiri Educatie si Stiinta', 'educatie-media', 'Educație',
                                            'Stiri Educatie', 'Stiri din Educatie si Invatamant']:
                            if 'Educatie' in articles_by_category_romania.keys():
                                articles_by_category_romania['Educatie'].append(article)
                            else:
                                articles_by_category_romania['Educatie'] = [article]
                        if categ in ['Locale', 'locale', 'Stiri Locale', 'locale-media', 'Sibiu', 'București', 'Craiova', 'Oradea', 'Orașul meu', 'Iași', 'Timișoara']:
                            if 'Locale' in articles_by_category_romania.keys():
                                articles_by_category_romania['Locale'].append(article)
                            else:
                                articles_by_category_romania['Locale'] = [article]
                        if categ in ['promo','Exclusiv', 'Vocile Digi', 'Be EU', 'Inedit',  'Adevăruri ascunse', 'Exces de putere','VREMEA - PROGNOZA METEO', 
                                            'RO 3.0', 'În fața națiunii', 'Articole', 'Republica Moldova', 'Meteo', 'Personalități',  'Diaspora', 'MOTIVARE', 'ENTR', 'Topuri', 'Decisiv','Horoscop']:
                            if 'Diverse' in articles_by_category_romania.keys():
                                articles_by_category_romania['Diverse'].append(article)
                            else:
                                articles_by_category_romania['Diverse'] = [article]
                        if categ in ['Justitie', 'justitie',  'Justiție']:
                            if 'Justitie' in articles_by_category_romania.keys():
                                articles_by_category_romania['Justitie'].append(article)
                            else:
                                articles_by_category_romania['Justitie'] = [article]

def get_articles_by_category_moldova():
    global moldova, articles_by_category_moldova
    for file in moldova:
        if file != 'cotidianul_articles.txt':
            with open(f"moldova/" + file, "rb") as f:
                articles = f.read().decode("utf-8").split('----------------------------------')
                for article in articles:
                    if article != '':
                        categ = article.split('\n')[3]
                        categ = categ.strip()
                        if len(categ.split()) <= 10 and len(categ.strip()) > 0:
                            if categ in ['Politica', 'Politic', 'Alegerile locale-2023', 'Electorala', 'Aderare UE','Politic național','Alegeri parlamentare 2019', 'Politică',
                                              'politic', 'Alegeri', 'Alegeri prezidențiale 2020', 'Electorala 2016', 'Alegeri locale 2023']:
                                if 'Politica' in articles_by_category_moldova.keys():
                                    articles_by_category_moldova['Politica'].append(article)
                                else:
                                    articles_by_category_moldova['Politica'] = [article]
                            if categ in ['Sport', 'sport']:
                                if 'Sport' in articles_by_category_moldova.keys():
                                    articles_by_category_moldova['Sport'].append(article)
                                else:
                                    articles_by_category_moldova['Sport'] = [article]
                            if categ in ['Economic', 'economic', 'Economie', 'economie']:
                                if 'Economie' in articles_by_category_moldova.keys():
                                    articles_by_category_moldova['Economie'].append(article)
                                else:
                                    articles_by_category_moldova['Economie'] = [article]
                            if categ in ['Social', 'social', 'Societate', 'societate']:
                                if 'Social' in articles_by_category_moldova.keys():
                                    articles_by_category_moldova['Social'].append(article)
                                else:
                                    articles_by_category_moldova['Social'] = [article]
                            if categ in ['Cultura', 'cultura', 'Cultură', 'cultură', 'Cultural']:
                                if 'Cultura' in articles_by_category_moldova.keys():
                                    articles_by_category_moldova['Cultura'].append(article)
                                else:
                                    articles_by_category_moldova['Cultura'] = [article]
                            if categ in ['Stiri', 'stiri', 'Știri', 'știri', 'Știri din Moldova', 'știri din Moldova', 'Actualitate', 'Săptămânal Panoramic','Internațional', 'În Lume',
                                              'Externe',  'Toate știrile', 'Internaţional', 'Războiul din Ucraina', 'Autorități publice locale']:
                                if 'Stiri' in articles_by_category_moldova.keys():
                                    articles_by_category_moldova['Stiri'].append(article)
                                else:
                                    articles_by_category_moldova['Stiri'] = [article]
                            if categ in ['Local', 'local', 'Locale', 'locale', 'CĂLĂRAȘI', 'Regional',  'UNGHENI - Știri din orașul și raionul Ungheni', ]:
                                if 'Locale' in articles_by_category_moldova.keys():
                                    articles_by_category_moldova['Locale'].append(article)
                                else:
                                    articles_by_category_moldova['Locale'] = [article]
                            if categ in ['Tehnologie', 'tehnologie', 'Tehnologie și știință', 'tehnologie și știință', 'IT şi Ştiinţă', 'Sci-tech', 'Statistică Pură', 'Cosmos']:
                                if 'Tehnologie' in articles_by_category_moldova.keys():
                                    articles_by_category_moldova['Tehnologie'].append(article)
                                else:
                                    articles_by_category_moldova['Tehnologie'] = [article]
                            if categ in ['Lifestyle', 'Life']:
                                if 'Lifestyle' in articles_by_category_moldova.keys():
                                    articles_by_category_moldova['Lifestyle'].append(article)
                                else:
                                    articles_by_category_moldova['Lifestyle'] = [article]
                            if categ in ['Justitie', 'justitie', 'Justiție', 'justiție']:
                                if 'Justitie' in articles_by_category_moldova.keys():
                                    articles_by_category_moldova['Justitie'].append(article)
                                else:
                                    articles_by_category_moldova['Justitie'] = [article]
                            if categ in ['Entertainment', 'Divertisment', 'Eurovision', 'Eveniment', 'Bibliotecarul & Cartea', 'Lectură', 'Foto / Video',  '#560']:
                                if 'Divertisment' in articles_by_category_moldova.keys():
                                    articles_by_category_moldova['Divertisment'].append(article)
                                else:
                                    articles_by_category_moldova['Divertisment'] = [article]
                            if categ in ['Educatie',  'Învățământ']:
                                if 'Educatie' in articles_by_category_moldova.keys():
                                    articles_by_category_moldova['Educatie'].append(article)
                                else:
                                    articles_by_category_moldova['Educatie'] = [article]
                            if categ in ['Important', 'Publicitate', 'Drepturile omului' ,'Special', 'Advertoriale',  'Astăzi Vă Prezentăm', 'Uncategorized',  'Investigații', 
                                              'Advertorial', 'Oameni care inspiră' , 'Slider',  'Ecologie', 'Cariera Mea', 'Judecați Singuri', 'Meteo', 'Urmează Apoi', 'Opinii', 'ExpresPlus',  
                                              'Diverse', '15.01.2024 - 10:50 ', 'Stop propaganda!', 'Diaspora', 'Comunitate', 'Istorie', '06.12.2023 - 16:15 ', 'Serioasă Problemă', 'Interviu', 
                                              'TOATE ARTICOLELE', 'PUB', '20.08.2021 - 11:28 ', 'Slider Principal',  'Reportaj',  'Transmisiuni și video',  'Horoscop']:
                                if 'Diverse' in articles_by_category_moldova.keys():
                                    articles_by_category_moldova['Diverse'].append(article)
                                else:
                                    articles_by_category_moldova['Diverse'] = [article]


get_articles_by_category_romania()
get_articles_by_category_moldova()

# print(categories_romania)
# print(categories_moldova)

def get_word_statistics_by_categ(categ_key, country):
    word_array = []
    if country == 'romania':
        articles_by_category = articles_by_category_romania
    else:
        articles_by_category = articles_by_category_moldova
    for article in articles_by_category[categ_key]:
        words = article.split()
        for word in words:
            word_array.append(len(word))
    word_array = np.array(word_array)
    return [np.mean(word_array), np.median(word_array), np.std(word_array)]

print("Statistics for Romania----------------------------------")
for categ in articles_by_category_romania.keys():
    print(f"Statistics for {categ}: {get_word_statistics_by_categ(categ, 'romania')}")
print("Statistics for Moldova----------------------------------")
for categ in articles_by_category_moldova.keys():
    print(f"Statistics for {categ}: {get_word_statistics_by_categ(categ, 'moldova')}")

# Make a csv file with the statistics
import csv

# Create a set of all categories
all_categories = set(articles_by_category_romania.keys()).union(articles_by_category_moldova.keys())

# Sort the categories
sorted_categories = sorted(list(all_categories))

# Open a new CSV file for writing
with open('statistics.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write the header row
    writer.writerow(['Country'] + sorted_categories)

    # Write a row for each country
    for country, articles_by_category in [('Romania', articles_by_category_romania), ('Moldova', articles_by_category_moldova)]:
        row = [country]
        for category in sorted_categories:
            if category in articles_by_category:
                stats = get_word_statistics_by_categ(category, country.lower())
                row.append(f'Mean: {stats[0]}, Median: {stats[1]}, Std dev: {stats[2]}')
            else:
                row.append('N/A')
        writer.writerow(row)

