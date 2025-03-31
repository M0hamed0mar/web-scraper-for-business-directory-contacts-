
import requests
from bs4 import BeautifulSoup
import csv

# Function to fetch the content of the page
def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an exception for 4xx/5xx errors
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None

# Function to parse the contact details from a page
def parse_contact_details(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    
    contacts = []
    
    # Extract business name (example: could vary based on site structure)
    business_name = soup.find('h1', class_='business-name-class')  # Update based on actual class or tag
    phone_number = soup.find('span', class_='phone-number-class')  # Update based on actual class or tag
    email = soup.find('a', href=lambda href: href and 'mailto:' in href)  # Assuming mailto links
    website = soup.find('a', href=True, class_='website-class')  # Update based on actual class or tag
    
    if business_name:
        contacts.append({
            'business_name': business_name.text.strip(),
            'phone_number': phone_number.text.strip() if phone_number else 'N/A',
            'email': email['href'].replace('mailto:', '').strip() if email else 'N/A',
            'website': website['href'].strip() if website else 'N/A',
        })
    
    return contacts

# Function to write the contacts to a CSV file
def save_contacts_to_csv(contacts, filename='contacts.csv'):
    keys = contacts[0].keys()  # Get the keys from the first contact record
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(contacts)

# Example usage
if __name__ == "__main__":
    url = "https://www.example.com/business-directory"  # Replace with the target URL
    page_content = fetch_page(url)
    
    if page_content:
        contact_details = parse_contact_details(page_content)
        
        if contact_details:
            save_contacts_to_csv(contact_details)
            print("Contact details saved successfully.")
        else:
            print("No contact details found.")
