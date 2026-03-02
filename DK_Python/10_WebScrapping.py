import requests
from bs4 import BeautifulSoup
import pandas as pd

# The URL of the website
url = "https://books.toscrape.com/"

# Fetch the webpage content
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all book containers
books = soup.find_all('article', class_='product_pod')

data = []

# Loop through each book to extract the required info
for book in books:
    # Book Name is stored in the 'title' attribute of the <a> tag inside <h3>
    name = book.h3.a['title']
    
    # Price is in a <p> tag with class 'price_color'
    price = book.find('p', class_='price_color').text.replace('Â', '')    
    # Stock status is in a <p> tag with class 'instock availability'
    stock = book.find('p', class_='instock availability').text.strip()
    
    data.append({
        "Book Name": name,
        "Price": price,
        "In Stock": stock
    })

# Create a DataFrame using pandas
df = pd.DataFrame(data)

# Export to Excel
df.to_excel("10_books.xlsx", index=False)

print("Data has been successfully scraped and saved to 10_books.xlsx")