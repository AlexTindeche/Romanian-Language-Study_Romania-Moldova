import sqlite3
from glob import glob


# Create a new SQLite database
conn = sqlite3.connect('news.db')
# Create table with newspaper, date, category, content
c = conn.cursor()
c.execute('''DROP TABLE IF EXISTS romania''')
c.execute('''CREATE TABLE romania
             (id INTEGER PRIMARY KEY AUTOINCREMENT, newspaper text, title text, date text, category text, content text)''')
c.execute('''DROP TABLE IF EXISTS moldova''')
c.execute('''CREATE TABLE moldova
             (id INTEGER PRIMARY KEY AUTOINCREMENT, newspaper text, title text, date text, category text, content text)''')


def txt_to_sql(txt_files, table_name):
    for file in txt_files:
        newspaper = file.split('/')[1].split('_')[0]
        print(newspaper)
        with open(file, 'r') as f:
            while title := f.readline().strip():
                # First article
                category = f.readline().strip()
                if category in ['Politic', 'politică', 'Politica', 'Politică', 'Stiri Politice Interne si Internationale', 'politic-extern',
                                            'politic-intern', 'Politica interna', 'Politica externa', 'Politica internă', 'Politica externă',
                                            'Opinie și promovare politică']:
                            category = 'Politica'
                elif category in ['Economic', 'economic', 'Economie', 'economie', 'Economia', 'economia', 'Economie si Afaceri',
                                    'Stiri Economice si Financiare','Companii', 'Bani și Afaceri','Business', 'Monitorizare Europarlamentare',
                                    'Parlamentul European']:
                    category = 'Economic'
                elif category in ['Social', 'social', 'Societate', 'societate', 'Societatea', 'societatea', 'Societate si Cultura',
                                    'Stiri Sociale si Culturale', 'Stiri Sociale', 'social/sanatate']:
                    category = 'Social'
                elif category in ['Sport', 'sport', 'Sporturi', 'sporturi', 'Sporturi si Turism', 'sporturi-turism', 'Stiri din Sport ',
                                    'Fotbal intern', 'Fotbal extern',]:
                    category = 'Sport'
                elif category in ['Cultura', 'cultura', 'Cultură', 'cultură', 'Cultura si Stiinta', 'cultura-stiinta', 'Stiri Culturale',
                                    'cultura-media']:
                    category = 'Cultura'
                elif category in ['Stiri Actuale', 'Actualitate', 'Stiri', 'Stiri Externe | Stiri Internationale', 'Ultimele Stiri',
                                    'International News','Știri Externe', 'News Hour with CNN', 'Știri România', 'Război în Israel',
                                    'Știri externe', 'Ştiri', 'Știri', 'externe', 'Externe', ]:
                    category = 'Stiri'
                elif category in ['Divertisment', 'divertisment', 'Divertisment si Utile', 'divertisment-utile', 'Stiri din Divertisment',
                                    'divertisment-media', 'Altceva Podcast', 'Film', 'entertainment', 'Mallcast', 'Muzică', 'Showbiz', 'Timp liber', 
                                    'Show', 'Vedete', 'Cancan', 'Life Show', 'eveniment']:
                    category = 'Divertisment'
                elif category in ['Tehnologie', 'tehnologie', 'Tehnologie si Stiinta', 'tehnologie-stiinta', 'Stiri Tehnologie si Stiinta',
                                    'tehnologie-media', 'Știinţă', 'High Tech', 'Auto / Tech', 'România Inteligentă', 'Sci-tech', 'Stiri Stiinta si Tehnologie', 'Tehnologie']:
                    category = 'Tehnologie'
                elif category in ['Sanatate', 'sanatate', 'Sănătate', 'sănătate', 'Sanatate si Familie', 'sanatate-familie', 'Stiri Sanatate si Familie',
                                    'sanatate-media', 'Stiri Sanatate', 'sanatate-media', 'Sănătate', 'Health','Stiri Sanatate',  'Sfat de sănătate']:
                    category = 'Sanatate'
                elif category in ['Auto', 'auto', 'Auto-Moto', 'auto-moto', 'Auto si Moto', 'auto-moto', 'Stiri Auto si Moto', 'auto-media', 'STOP TRAFIC', 
                                    'Transporturi']:
                    category = 'Auto'
                elif category in ['Turism', 'turism', 'Turism si Vacante', 'turism-vacante', 'Stiri Turism si Vacante', 'turism-media', 'Turism si Vacante',
                                'Travel']:
                    category = 'Turism'
                elif category in ['Lifestyle', 'lifestyle', 'Lifestyle si Utile', 'lifestyle-utile', 'Stiri Lifestyle si Utile', 'lifestyle-media', 'Lifestyle',
                                    'Life',  'Stil de viață', 'Stiri Lifestyle']:
                    category = 'Lifestyle'
                elif category in ['Educatie', 'educatie', 'Educatie si Stiinta', 'educatie-stiinta', 'Stiri Educatie si Stiinta', 'educatie-media', 'Educație',
                                    'Stiri Educatie', 'Stiri din Educatie si Invatamant']:
                    category = 'Educatie'
                elif category in ['Locale', 'locale', 'Stiri Locale', 'locale-media', 'Sibiu', 'București', 'Craiova', 'Oradea', 'Orașul meu', 'Iași', 'Timișoara']:
                    category = 'Locale'
                elif category in ['Justitie', 'justitie',  'Justiție']:
                    category = 'Justitie'
                elif category in ['promo','Exclusiv', 'Vocile Digi', 'Be EU', 'Inedit',  'Adevăruri ascunse', 'Exces de putere','VREMEA - PROGNOZA METEO', 
                                    'RO 3.0', 'În fața națiunii', 'Articole', 'Republica Moldova', 'Meteo', 'Personalități',  'Diaspora', 'MOTIVARE', 'ENTR', 'Topuri', 'Decisiv','Horoscop']:
                    category = 'Diverse'
                elif category in ['Politica', 'Politic', 'Alegerile locale-2023', 'Electorala', 'Aderare UE','Politic național','Alegeri parlamentare 2019', 'Politică',
                                              'politic', 'Alegeri', 'Alegeri prezidențiale 2020', 'Electorala 2016', 'Alegeri locale 2023']:
                    category = 'Politica'
                elif category in ['Sport', 'sport']:
                    category = 'Sport'
                elif category in ['Economic', 'economic', 'Economie', 'economie']:
                    category = 'Economic'
                elif category in ['Social', 'social', 'Societate', 'societate']:
                    category = 'Social'
                elif category in ['Cultura', 'cultura', 'Cultură', 'cultură', 'Cultural']:
                    category = 'Cultura'
                elif category in ['Stiri', 'stiri', 'Știri', 'știri', 'Știri din Moldova', 'știri din Moldova', 'Actualitate', 'Săptămânal Panoramic','Internațional', 'În Lume',
                                    'Externe',  'Toate știrile', 'Internaţional', 'Războiul din Ucraina', 'Autorități publice locale']:
                    category = 'Stiri'
                elif category in ['Local', 'local', 'Locale', 'locale', 'CĂLĂRAȘI', 'Regional',  'UNGHENI - Știri din orașul și raionul Ungheni', ]:
                    category = 'Locale'
                elif category in ['Tehnologie', 'tehnologie', 'Tehnologie și știință', 'tehnologie și știință', 'IT şi Ştiinţă', 'Sci-tech', 'Statistică Pură', 'Cosmos']:
                    category = 'Tehnologie'
                elif category in ['Lifestyle', 'Life']:
                    category = 'Lifestyle'
                elif category in ['Justitie', 'justitie', 'Justiție', 'justiție']:
                    category = 'Justitie'
                elif category in ['Entertainment', 'Divertisment', 'Eurovision', 'Eveniment', 'Bibliotecarul & Cartea', 'Lectură', 'Foto / Video',  '#560']:
                    category = 'Divertisment'
                elif category in ['Educatie',  'Învățământ']:
                    category = 'Educatie'
                else:
                    category = 'Diverse'
                date = f.readline().strip()
                
                content = []
                # Read until ----------------------------------
                while True:
                    line = f.readline().strip()
                    if line.startswith('----------------------------------'):
                        f.readline()
                        break
                    content.append(line)
                    
                # Add to database
                c.execute(f"INSERT INTO {table_name} (newspaper, title, date, category, content) VALUES (?, ?, ?, ?, ?)", (newspaper, title, date, category, ' '.join(content)))
                conn.commit()

romania_files = glob('romania/*.txt')
print(romania_files)
txt_to_sql(romania_files, 'romania')

moldova_files = glob('moldova/*.txt')
txt_to_sql(moldova_files, 'moldova')

conn.close()





        
    
