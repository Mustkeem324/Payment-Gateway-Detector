from bs4 import BeautifulSoup
import re
from fake_useragent import UserAgent
import concurrent.futures
import time
import requests

def get_random_user_agent():
    ua = UserAgent()
    return ua.random

def check_gateway(url):
    try:
        headers = {'User-Agent': get_random_user_agent()}
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status() 
    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return None
    bsoup = BeautifulSoup(response.text, 'html.parser')

    payment_gateways = {
        'stripe': ['script', {'src': re.compile(r'.*js\.stripe\.com.*')}, {'src': re.compile(r'.*stripe.*')}],
        'paypal': ['script', {'src': re.compile(r'.*paypal.*')}, {'src': re.compile(r'.*checkout\.paypal\.com.*')}, {'src': re.compile(r'.*paypalobjects.*')}],
        'braintree': ['script', {'src': re.compile(r'.*braintree.*')}, {'src': re.compile(r'.*braintreegateway.*')}],
        'worldpay': ['script', {'src': re.compile(r'.*worldpay.*')}],
        'authnet': ['script', {'src': re.compile(r'.*authorizenet.*')}, {'src': re.compile(r'.*authorize\.net.*')}],
        'recurly': ['script', {'src': re.compile(r'.*recurly.*')}],
        'shopify': ['script', {'src': re.compile(r'.*shopify.*')}],
        'square': ['script', {'src': re.compile(r'.*square.*')}],
        'cybersource': ['script', {'src': re.compile(r'.*cybersource.*')}],
        'adyen': ['script', {'src': re.compile(r'.*adyen.*')}],
        '2checkout': ['script', {'src': re.compile(r'.*2checkout.*')}],
        'authorize.net': ['script', {'src': re.compile(r'.*authorize\.net.*')}],
        'worldpay': ['script', {'src': re.compile(r'.*worldpay.*')}],
        'eway': ['script', {'src': re.compile(r'.*eway.*')}],
        'bluepay': ['script', {'src': re.compile(r'.*bluepay.*')}],
    }

    detected_gateway = None

    for pg, patterns in payment_gateways.items():
        script_elements = bsoup.find_all('script', {'src': patterns[1]['src']}) if len(patterns) > 1 else []
        script_elements += bsoup.find_all('script', {'src': patterns[2]['src']}) if len(patterns) > 2 else []
        script_elements += bsoup.find_all('script', {'src': patterns[3]['src']}) if len(patterns) > 3 else []

        if bsoup.find(*patterns) or any(script_element for script_element in script_elements) or bsoup.find(string=re.compile(rf'.*{pg}.*', re.IGNORECASE)):
            detected_gateway = pg
            break

    return url, detected_gateway

def add_https_if_missing(url):
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://' + url
    return url

token = 'Your token'
chat_id = 'your chat-id'

def send_message(url, gateway):
    if gateway:
        msg = f'<b>{url}:</b> <code>{gateway}</code>'
        requests.get(f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={msg}&parse_mode=HTML')
        print(msg)

def process_url(url):
    url = url.strip()
    url = add_https_if_missing(url)

    try:
        result = check_gateway(url)
        if result and result[1]:  
            url, gateway = result
            send_message(url, gateway)
    except Exception as e:
        print(f"Error processing {url}: {e}")

def main():
    with open('urls.txt', 'r') as file:
        urls = file.readlines()
    workers = min(10, len(urls))
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        executor.map(process_url, urls)

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")
