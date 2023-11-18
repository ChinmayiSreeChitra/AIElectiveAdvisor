import requests
from bs4 import BeautifulSoup

# URL of the page to scrape
url = "https://catalog.fullerton.edu/preview_course_nopop.php?catoid=80&coid=540413"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all <p> tags
    p_tags = soup.find_all('p')

    # Extract and print the text from each <p> tag
    for p in p_tags:
        print(p.get_text(strip=True))

else:
    print("Failed to retrieve the page. Status code:", response.status_code)
