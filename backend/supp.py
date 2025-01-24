#!/usr/bin/env python3

import ssl
import certifi

# Use certifi's SSL certificates
ssl._create_default_https_context = ssl.create_default_context(cafile=certifi.where())


import requests
from bs4 import BeautifulSoup
import sqlite3
import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


# use stopwords to tokenize the data
stop_words = set(stopwords.words('english'))

# connect to the database
conn = sqlite3.connect('backend/herbs.db')
c = conn.cursor()

def clean_description(description):
    return re.sub(r'\[\d+\]', '', description).strip()

def insert_herb(common_name, scientific_name):
    c.execute('INSERT INTO herbs (common_name, scientific_name) VALUES (?, ?)', (common_name, scientific_name))
    return c.lastrowid

def insert_use(description):
    c.execute('INSERT OR IGNORE INTO uses (description) VALUES (?)', (description,))
    c.execute('SELECT id FROM uses WHERE description = ?', (description,))
    return c.fetchone()[0]

def link_herb_to_use(herb_id, use_id):
    c.execute('INSERT INTO herb_use (herb_id, use_id) VALUES (?, ?)', (herb_id, use_id))

def extract_keywords(text):
    words = word_tokenize(text.lower())
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
    return set(filtered_words)

def process_uses(uses_text, herb_id):
    keywords = extract_keywords(uses_text)
    for keyword in keywords:
        use_id = insert_use(keyword)
        link_herb_to_use(herb_id, use_id)

        
url = 'https://en.wikipedia.org/wiki/List_of_plants_used_in_herbalism'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
entries = soup.find_all('table', {'class': 'wikitable sortable'})

for table in entries:
    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')
        if len(cells) > 1:
            common_name = cells[0].text.strip()
            scientific_name = cells[1].text.strip()
            uses = cells[2].text.strip() if len(cells) > 2 else 'No description'
            herb_id = insert_herb(common_name, scientific_name)
            process_uses(uses, herb_id)

conn.commit()
conn.close()
print("Data scraped and stored successfully.")
