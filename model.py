import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    return response.text


def parse_restaurant_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    data = []
    try:
        _extracted_from_parse_restaurant_data_(soup, data)
    except AttributeError as e:
            logging.warning(f"Lỗi khi phân tích dữ liệu nhà hàng: {e}")
    return data


# TODO Rename this here and in `parse_restaurant_data`
def _extracted_from_parse_restaurant_data_(soup, data):
    rating = _extracted_from__extracted_from_parse_restaurant_data__3(
        soup, 'review-points green', "Không tìm thấy thẻ đánh giá."
    )
    # Tìm tên nhà hàng
    name_tag = soup.find('div', class_='title fd-text-ellip')
    restaurant_name = None
    if name_tag:
        if a_tag := name_tag.find('a'):
            restaurant_name = a_tag.get_text(strip=True)
        else:
            print("Không tìm thấy thẻ <a> trong thẻ tên nhà hàng.")
    else:
        print("Không tìm thấy thẻ tên nhà hàng.")

    address = _extracted_from__extracted_from_parse_restaurant_data__3(
        soup, 'desc fd-text-ellip ng-binding', "Không tìm thấy thẻ địa chỉ."
    )
    data.append({
        'Name': restaurant_name,
        'Address': address,
        'Rating': rating
    })


# TODO Rename this here and in `_extracted_from_parse_restaurant_data_`
def _extracted_from__extracted_from_parse_restaurant_data__3(soup, class_, arg2):
    # Tìm rating
    rating_tag = soup.find('div', class_=class_)
    result = None
    if rating_tag:
        result = rating_tag.get_text(strip=True)
    else:
        print(arg2)

    return result


def crawl_foody(base_url,max_pages=20):
    base_url = base_url
    all_data = []
    
    for page in range(1, max_pages + 1):
        url = f'{base_url}?page={page}'
        logging.info(f'Đang crawl trang {page}...')
        html = get_page(url)
        if html is None:
            continue
        page_data = parse_restaurant_data(html)
        all_data.extend(page_data)
        logging.info(f'Tìm thấy {len(page_data)} nhà hàng trên trang {page}')
        
        if len(page_data) == 0:
            logging.info('Không còn dữ liệu. Dừng crawl...')
            break
        
        time.sleep(random.uniform(2, 5))
    
    return all_data
