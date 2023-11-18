import requests
from bs4 import BeautifulSoup
import re
import sqlite3

# Create a SQLite database (or connect to an existing one)
conn = sqlite3.connect('scraped_data.db')
cursor = conn.cursor()

# Create the 'scraped_data' table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS scraped_data (
        id INTEGER PRIMARY KEY,
        coid INTEGER,
        data TEXT
    )
''')
conn.commit()

# List of coid numbers
coid_numbers = [
    540413, 540423, 540414, 540421, 540415, 540676, 540409, 540407, 540410,
    540408, 540416, 540420, 541020, 540412, 540417, 540411, 540418, 540424,
    541009, 541043, 540419, 541010, 540930, 540422, 540425, 540974, 540701
]

# Iterate through the list of coid numbers
for coid in coid_numbers:
    # Generate the URL for each coid number
    url = f"https://catalog.fullerton.edu/preview_course_nopop.php?catoid=80&coid={coid}"

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all <p> tags
        p_tags = soup.find_all('p')

        # Extract and store the text from each <p> tag
        text_data = ""
        for p in p_tags:
            text = p.get_text(strip=True)
            text_data += text + "\n"

        # Insert the scraped data into the database
        cursor.execute("INSERT INTO scraped_data (coid, data) VALUES (?, ?)", (coid, text_data))
        conn.commit()

    else:
        print(f"Failed to retrieve the page for coid {coid}. Status code:", response.status_code)

# Close the database connection
conn.close()
