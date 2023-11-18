import requests
from bs4 import BeautifulSoup
import pandas as pd

# List of prefixes
prefixes = ["ACCT", "AFAM", "AGNG", "AMST", "ANTH", "ARAB", "ART", "ARTE", "ASAM", "ASTR", "BIOL", "BUAD", "CAS",
            "CEDU", "CHEM", "CHIC", "CHIN", "CNSM", "COMD", "COMM", "COUN", "CPLT", "CPSC", "CRJU", "CTVA", "DANC",
            "ECON", "EDAD", "EDD", "EDEL", "EDSC", "EGCE", "EGEC", "EGGN", "EGME", "EGMT", "ENED", "ENGL", "ENST",
            "ESE", "ESM", "ETHN", "FIN", "FREN", "GEOG", "GEOL", "GRMN", "HCOM", "HIST", "HONR", "HSS", "HUSR", "IDT",
            "ISDS", "ITAL", "JAPN", "KNES", "KORE", "LBST", "LING", "LTAM", "MAED", "MATH", "MGMT", "MKTG", "MLNG",
            "MLSC", "MSW", "MUS", "MUSE", "NURS", "PERS", "PHIL", "PHYS", "PORT", "POSC", "PSYC", "PUBH", "READ",
            "RLST", "SCED", "SOCI", "SPAN", "SPED", "TESL", "THTR", "VIET", "WGST"]

# Create an empty list to store the coid numbers
coid_numbers = []

# The URL of the website you want to scrape
base_url = "https://catalog.fullerton.edu/content.php?filter%5B27%5D={}&filter%5B29%5D=&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=80&expand=&navoid=11056&search_database=Filter&filter%5Bexact_match%5D=1#acalog_template_course_filter"

# Loop through the prefixes
for prefix in prefixes:
    # Construct the URL for the specific prefix
    url = base_url.format(prefix)

    # Send a GET request to the website
    response = requests.get(url)

    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the 'a' tags that contain 'coid' in their 'href' attribute
    coid_links = soup.find_all('a', href=lambda href: href and 'coid' in href)

    # Extract the 'coid' numbers from the 'href' attributes of the links and add them to the list
    coid_numbers.extend(link.get('href').split('=')[-1] for link in coid_links)

# Create a DataFrame with the coid numbers
df = pd.DataFrame({'coid Numbers': coid_numbers})

# Save the DataFrame to an Excel file
df.to_excel('coid_numbers1.xlsx', index=False)
