#!/usr/bin/env python3

import sqlite3
import sys
import nltk
from nltk.stem import PorterStemmer

nltk.download('punkt')

# Porter Stemmer
ps = PorterStemmer()

def find_remedies(symptom):

    conn = sqlite3.connect('backend/herbs.db')
    c = conn.cursor()

    symptom_keywords = symptom.lower().split()
    print(f"Processing symptoms (stemmed): {symptom_keywords}")  

    # applying stemming
    stemmed_keywords = [ps.stem(keyword) for keyword in symptom_keywords]
    print(f"Stemmed keywords: {stemmed_keywords}")  

    query = """
        SELECT DISTINCT herbs.common_name, herbs.scientific_name
        FROM herbs
        JOIN herb_use ON herbs.id = herb_use.herb_id
        JOIN uses ON herb_use.use_id = uses.id
        WHERE "uses".description LIKE ?
    """

    results = set() 
    for keyword in stemmed_keywords:
        c.execute(query, (f"%{keyword}%",))
        rows = c.fetchall()

        for row in rows:
            results.add(f"{row[0]} ({row[1]})")

    conn.close()

    if results:
        print("Matching remedies found:", results) 
        return "\n".join(results)
    else:
        print("No remedies found.")
        return "No remedies found for your symptoms."

if __name__ == "__main__":
    user_input = " ".join(sys.argv[1:])
    remedies = find_remedies(user_input)
    print(remedies)
