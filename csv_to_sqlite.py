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





        
    
