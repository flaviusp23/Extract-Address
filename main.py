import pandas as pd
import requests
from bs4 import BeautifulSoup
import pyap
import json
import threading
import difflib

lock = threading.Lock()

continue_running = True

def remove_similar_addresses(parsed_addresses):
    unique_addresses = []
    for domain, addresses in parsed_addresses.items():
        unique_domain_addresses = []
        for address in addresses:
            is_unique = True
            for unique_address in unique_domain_addresses:
                similarity_ratio = difflib.SequenceMatcher(None, address['full_address'], unique_address['full_address']).ratio()
                if similarity_ratio > 0.9:
                    is_unique = False
                    break
            if is_unique:
                unique_domain_addresses.append(address)
        unique_addresses.append((domain, unique_domain_addresses))
    return dict(unique_addresses)


def parse_address(addr):
    address = pyap.parse(addr, country="US")
    if not address:
        address = pyap.parse(addr, country="GB")
    if not address:
        address = pyap.parse(addr, country="CA")
    return address[0] if address else None

def extract_and_parse_addresses(website):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
        }
        result = requests.get(website, headers=headers, timeout=(5,3))
        result.raise_for_status()
        content = result.text
        soup = BeautifulSoup(content, 'lxml')

        text_content = soup.get_text()

        text_content_lines = [line for line in text_content.split('\n') if line.strip()]

        text_content = '\n'.join(text_content_lines)

        addresses = parse_address(text_content)

        parsed_addresses = []
        if addresses:
            address_dict = addresses.as_dict()
            filtered_address = {
                'full_address': address_dict.get('full_address', ''),
                'country': address_dict.get('country_id', ''),
                'region': address_dict.get('region1', ''),
                'city': address_dict.get('city', ''),
                'postcode': address_dict.get('postal_code', ''),
                'road': f"{address_dict.get('street_name', '')} {address_dict.get('street_type', '')}",
                'road_numbers': address_dict.get('street_number', '')
            }
            parsed_addresses.append(filtered_address)
        return parsed_addresses
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while processing {website}")
        return []

def process_website(domain):
    protocols = ['http://', 'https://']
    prefixes = ['', 'www.']

    for protocol in protocols:
        for prefix in prefixes:
            website = f"{protocol}{prefix}{domain}"
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
                }
                result = requests.head(website, headers=headers, timeout=5)
                if result.status_code < 400:
                    print(f"{website} is working. Parsing addresses...")
                    addresses = extract_and_parse_addresses(website)
                    with lock:
                        parsed_addresses[website] = addresses  
                    return  
                else:
                    print(f"{website} is not reachable.")
            except requests.exceptions.RequestException as e:
                print(f"Error occurred while processing {website}")
                continue


def read_and_parse_websites(file_path):
    content = pd.read_parquet(file_path)
    global parsed_addresses
    parsed_addresses = {}
    threads = []

    for index, row in content.iterrows():
        if not continue_running:
            break
        domain = row['domain']
        thread = threading.Thread(target=process_website, args=(domain,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    
    return parsed_addresses

file_path = "list of company websites.snappy.parquet"
output_csv = "parsed_addresses.csv"

parsed_addresses = read_and_parse_websites(file_path)
unique_addresses = remove_similar_addresses(parsed_addresses)
with open(output_csv, 'w') as file:
    file.write("website,parsed_addresses\n") 
    for website, addresses in unique_addresses.items():
        for address in addresses:
            file.write(f"{website},{json.dumps(address)}\n")

print(f"Parsed addresses have been exported to {output_csv}")
