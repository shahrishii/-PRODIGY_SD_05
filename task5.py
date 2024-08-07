import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape product data from Flipkart
def scrape_flipkart_products(url):
    # Send HTTP request to the URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve data from {url}")
        return []

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find product elements
    products = soup.find_all('div', class_='_1AtVbE')
    
    data = []
    for product in products:
        # Extract product details
        name_tag = product.find('a', class_='IRpwTa')
        price_tag = product.find('div', class_='_30jeq3')
        rating_tag = product.find('div', class_='_3LWZlK')
        
        name = name_tag.get_text(strip=True) if name_tag else 'N/A'
        price = price_tag.get_text(strip=True) if price_tag else 'N/A'
        rating = rating_tag.get_text(strip=True) if rating_tag else 'N/A'
        
        # Append data to the list
        data.append({
            'Name': name,
            'Price': price,
            'Rating': rating
        })

    return data

# Function to save data to CSV
def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# Example URL for Flipkart (replace with the actual URL you want to scrape)
url = 'https://www.flipkart.com/laptops/pr?sid=6bo%2Cb5g'

# Scrape product data
product_data = scrape_flipkart_products(url)

# Save data to CSV
if product_data:
    save_to_csv(product_data, 'flipkart_products.csv')
