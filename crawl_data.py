# -*- coding: utf-8 -*-
#------------ ĐOẠN 1--------------------------------
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, StaleElementReferenceException,NoSuchElementException,WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from bs4 import BeautifulSoup
import requests
import os
import hashlib
from PIL import Image
from io import BytesIO
import unicodedata
import re
"""
def get_request(url): 
    # Gửi yêu cầu GET tới URL
        response = requests.get('https://www.foody.vn/')
        if response.status_code != 200:
            print(f"Không thể truy cập trang web. Mã trạng thái: {response.status_code}")
                

        # Phân tích nội dung HTML
        driver = webdriver.Chrome()
        driver.get('https://www.foody.vn/')
        # Đăng nhập 
        login('https://www.foody.vn/',"trantrongkhang0941@gmail.com", "0833030679")"""
    
#đăng nhập vào hệ thống
def login(url,username, password):
    driver.get(url)
    
    try:
        # Click vào nút đăng nhập
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[ng-click='Login()']"))
        )
        login_button.click()
        
        # Đợi form đăng nhập xuất hiện
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Email"))
        )
        
        # Nhập thông tin đăng nhập
        driver.find_element(By.ID, "Email").send_keys(username)
        driver.find_element(By.ID, "Password").send_keys(password)
        
        # Click nút đăng nhập bằng cách sử dụng ID
        driver.find_element(By.ID, "bt_submit").click()
        
        # Đợi cho đến khi đăng nhập thành công
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[ng-click='Logout()']"))
        )
        
        print("Đăng nhập thành công!")
    except Exception as e:
        print(f"Đăng nhập thất bại: {str(e)}")
        
def close_popups():
    try:
        # Tìm và đóng các pop-up hoặc quảng cáo (điều chỉnh selector nếu cần)
        close_buttons = driver.find_elements(By.CSS_SELECTOR, ".close-button, .ad-close")
        for button in close_buttons:
            button.click()
    except:
        pass
#click vào xem thêm để load
def scroll_and_wait():
    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    return new_height != last_height

def click_load_more():
    try:
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.fd-btn-more"))
        )
        if not element.is_displayed():
            return False
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        time.sleep(random.uniform(1.5, 3.5))
        driver.execute_script("arguments[0].click();", element)
        time.sleep(5)  # Đợi sau khi click
        return True
    except (TimeoutException, ElementClickInterceptedException, StaleElementReferenceException, NoSuchElementException):
        return False

def wait_for_page_load():
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.row.ng-scope"))
    )
    
def crawl_res_data():
    restaurants = driver.find_elements(By.CSS_SELECTOR, "div.row.ng-scope")
    data = []
    for restaurant in restaurants:
        try:
            name = restaurant.find_element(By.CSS_SELECTOR, "div.title.fd-text-ellip a").text
            address = restaurant.find_element(By.CSS_SELECTOR, "div.desc.fd-text-ellip.ng-binding").text
            
            try:
                rating = restaurant.find_element(By.CSS_SELECTOR, "div.point.ng-binding").text
            except NoSuchElementException:
                rating = "N/A"
            
            data.append({
                "Name": name,
                "Address": address,
                "Rating": rating
            })
        except Exception as e:
            print(f"Lỗi khi crawl dữ liệu nhà hàng: {str(e)}")
    return data

def crawl_on_page():

    # Tìm các phần tử sau khi JavaScript đã tải xong
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')    

    # Tìm tất cả các phần tử chứa thông tin nhà hàng
    restaurant_items = soup.find_all('div', class_='microsite-top-points')
    restaurants_data = []

    for item in restaurant_items:
        # Tìm rating
        rating_tag = item.find('div', class_='review-points')
        rating = rating_tag.get_text(strip=True) if rating_tag else None

        # Tìm tên nhà hàng
        name_tag = item.find('div', class_='title fd-text-ellip')
        restaurant_name = name_tag.find('a').get_text(strip=True) if name_tag and name_tag.find('a') else None

        # Tìm địa chỉ
        address_tag = item.find('div', class_='desc fd-text-ellip ng-binding')
        address = address_tag.get_text(strip=True) if address_tag else None

        # Thêm thông tin vào danh sách
        restaurants_data.append((rating, restaurant_name, address))

    return restaurants_data

def crawl_many_pages():
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    res_summary = soup.find('div', id='res-summary-point')
    
    if res_summary:
        rating_items = res_summary.find_all('div', class_='microsite-top-points')
        
        ratings = {}
        for item in rating_items:
            label = item.find('div', class_='label').text.strip()
            value = item.find('span', class_='avg-txt-highlight').text.strip()
            ratings[label] = value
        
        restaurant_name = soup.find('h1', class_='main-info-title').text.strip() if soup.find('h1', class_='main-info-title') else "N/A"
        address = soup.find('div', class_='res-common-add').text.strip() if soup.find('div', class_='res-common-add') else "N/A"

        restaurant_data = (
            restaurant_name,
            address,
            ratings.get('Chất lượng', 'N/A'),
            ratings.get('Phục vụ', 'N/A'),
            ratings.get('Giá cả', 'N/A'),
            ratings.get('Vị trí', 'N/A'),
            ratings.get('Không gian', 'N/A')
        )

        return [restaurant_data]
    else:
        print("Không tìm thấy thông tin đánh giá trên trang.")
        return []

def open_restaurant_in_new_tab(link, main_window_handle, max_retries=3, wait_time=30):
    """
    Mở nhà hàng trong tab mới và đảm bảo quay lại tab chính sau khi hoàn tất.
    """
    for attempt in range(max_retries):
        try:
            # Ghi log thông tin đang thử mở trang
            print(f"Attempt {attempt + 1}: Opening restaurant page {link}")

            # Mở một tab mới
            driver.execute_script("window.open('');")
            
            # Chuyển sang tab mới
            driver.switch_to.window(driver.window_handles[-1])
            
            # Điều hướng đến trang nhà hàng
            driver.get(link)

            # Đợi trang tải xong
            WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.micro-detail"))
            )
            
            print(f"Successfully opened restaurant page in new tab (attempt {attempt + 1})")
            return True
        
        except (TimeoutException, WebDriverException) as e:
            print(f"Error opening restaurant page (attempt {attempt + 1}): {str(e)}")
            
            # Đóng tab hiện tại nếu mở không thành công
            if len(driver.window_handles) > 1:
                driver.close()
            
            # Chuyển lại về tab chính
            driver.switch_to.window(main_window_handle)

            if attempt == max_retries - 1:
                print(f"Failed to open restaurant page after {max_retries} attempts")
                return False
            
            # Đợi trước khi thử lại
            time.sleep(3)

def close_current_tab_and_return_to_main(main_window_handle):
    """
    Đóng tab hiện tại và quay lại tab chính
    """
    try:
        # Đóng tab hiện tại
        driver.close()
        
        # Chuyển về tab chính
        driver.switch_to.window(main_window_handle)
        
        print("Closed restaurant tab and returned to main tab")
        return True
    except Exception as e:
        print(f"Error closing tab and returning to main: {str(e)}")
        return False
        

def process_restaurant_item(url, output_folder=None, max_images=None):
        
    image_count = 0
    processed_hashes = set()  # Set to store processed image hashes

    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find all restaurant elements
    restaurant_items = soup.find_all('div', class_='content-item ng-scope')
    
    for item in restaurant_items:
        try:
            # Extract restaurant name
            name_tag = item.find('div', class_='title fd-text-ellip')
            restaurant_name = name_tag.find('a').get_text(strip=True) if name_tag and name_tag.find('a') else None                

            # Find image element
            img_tag = item.find('div', class_='avatar').find('img')
            img_url = img_tag.get('src') if img_tag else None
            
            if img_url:
                img_url = process_url(img_url, url)
                response = requests.get(img_url)
                img_data = response.content
                img_hash = get_image_hash(img_data)
                
                if img_hash not in processed_hashes:
                    # Use restaurant name in the filename
                    safe_name = "".join([c for c in restaurant_name if c.isalpha() or c.isdigit() or c==' ']).rstrip()
                    img_filename = f'{output_folder}/{safe_name}_{image_count}.jpg'
                    
                    with open(img_filename, 'wb') as handler:
                        handler.write(img_data)
                    print(f"Đã tải xuống: {img_url}")
                    print(f"Nhà hàng: {restaurant_name}")
                    
                    processed_hashes.add(img_hash)
                    image_count += 1
                else:
                    print(f"Ảnh trùng lặp bỏ qua: {img_url}")
            
            if max_images is not None and image_count >= max_images:
                print(f"Đã đạt đến giới hạn {max_images} ảnh.")
                return
            print(f"Hoàn thành việc scrape hình ảnh! Đã xử lý {len(image_count)} hình ảnh")
        except Exception as e:
            print(f"Lỗi khi xử lý nhà hàng: {e}")

    
def process_url(img_url, base_url):
    if img_url.startswith('//'):
        return 'https:' + img_url
    elif not img_url.startswith(('http:', 'https:')):
        return base_url + img_url if img_url.startswith('/') else base_url + '/' + img_url
    return img_url 
def get_image_hash(image_data):
    image = Image.open(BytesIO(image_data))
    image = image.resize((8, 8), Image.LANCZOS).convert('L')
    pixels = list(image.getdata())
    avg = sum(pixels) / len(pixels)
    return ''.join('1' if pixel > avg else '0' for pixel in pixels)
def remove_diacritics(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))

def sanitize_filename(filename):
    # Remove diacritics and convert to lowercase
    filename = remove_diacritics(filename.lower())
    # Replace spaces with underscores and remove non-alphanumeric characters
    filename = re.sub(r'[^a-z0-9_]+', '', filename.replace(' ', '_'))
    return filename
#----------------------------------Main-----------------------------------
def scrabing(max_attempts=3, max_pages=10, columns_name=None,wait_time=5):
    all_data = []
    page = 0    
    # Lưu handle của tab chính
    main_window_handle = driver.current_window_handle
    while page < max_pages:
        try:
            close_popups()  # Đảm bảo popup không làm gián đoạn
            
            # Tìm tất cả các link nhà hàng trên trang hiện tại
            restaurant_links = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.title.fd-text-ellip a"))
            )
            crawled_urls = set()  # Set để lưu các URL đã được crawl
            # Lưu các URL nhà hàng chưa được crawl
            restaurant_urls = [link.get_attribute('href') for link in restaurant_links if link.get_attribute('href') not in crawled_urls]
            
            # Chạy qua các URL chưa được crawl
            for url in restaurant_urls:
                # Đánh dấu URL đã được crawl sau khi thành công
                crawled_urls.add(url)
                print(crawled_urls)
                if url in crawled_urls:
                    print(f"URL {url} đã được crawl. Bỏ qua...")
                    continue
                # Chỉ mở tab nếu URL chưa được crawl
                if open_restaurant_in_new_tab(url, main_window_handle,2,20):
                    restaurant_data = crawl_many_pages()
                    
                    if restaurant_data:
                        all_data.extend(restaurant_data)
                        print(f"Đã thu thập thông tin từ nhà hàng. Tổng số nhà hàng: {len(all_data)}")
                    else:
                        print("Không thể thu thập dữ liệu nhà hàng.")
                                        
                    # Đóng tab hiện tại và quay lại trang chính
                    if not close_current_tab_and_return_to_main(main_window_handle):
                        print("Không thể quay lại trang chính. Thử làm mới trang.")
                        driver.refresh()
                
                time.sleep(wait_time)  # Nghỉ giữa các lần mở tab

            
        except Exception as e:
            print(f"Error during crawling: {str(e)}")
        
        success = False
        for attempt in range(max_attempts):
            if click_load_more():
                success = True
                break
            else:
                print(f"Không thể click 'Xem thêm' lần thứ {attempt + 1}. Thử lại lần {attempt + 1}/{max_attempts}")
                time.sleep(2)
        
        if success:
            page += 1
            print(f"Đã chuyển sang trang {page + 1}")
        else:
            print(f"Không thể click 'Xem thêm' sau {max_attempts} lần thử. Dừng crawl.")
            break

    # Tạo DataFrame từ dữ liệu đã thu thập
    df = pd.DataFrame(all_data, columns=columns_name)
    print(df.head())
    return df

def scrab_img(url, output_folder=None, wait_time=5, max_images=None, max_pages=None):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    try:
        time.sleep(wait_time)
        
        page = 0
        image_count = 0
        processed_hashes = set()  # Set to store processed image hashes

        while page < max_pages:
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            # Find all restaurant elements
            restaurant_items = soup.find_all('div', class_='content-item ng-scope')
            
            for item in restaurant_items:
                try:
                    # Extract restaurant name
                    name_tag = item.find('div', class_='title fd-text-ellip')
                    restaurant_name = name_tag.find('a').get_text(strip=True) if name_tag and name_tag.find('a') else None        

                    # Find image element
                    img_tag = item.find('div', class_='avatar').find('img')
                    img_url = img_tag.get('src') if img_tag else None
                    
                    if img_url:
                        img_url = process_url(img_url, url)
                        response = requests.get(img_url)
                        img_data = response.content
                        img_hash = get_image_hash(img_data)
                        
                        if img_hash not in processed_hashes:
                            # Use restaurant name in the filename
                            safe_name = sanitize_filename(restaurant_name)
                            img_filename = f'{output_folder}/{safe_name}_{image_count}.jpg'
                            
                            with open(img_filename, 'wb') as handler:
                                handler.write(img_data)
                            print(f"Đã tải xuống: {img_url}")
                            print(f"Nhà hàng: {safe_name}")
                            
                            processed_hashes.add(img_hash)
                            image_count += 1
                        else:
                            print(f"Ảnh trùng lặp bỏ qua: {img_url}")
                    
                    if max_images is not None and image_count >= max_images:
                        print(f"Đã đạt đến giới hạn {max_images} ảnh.")
                        return
                except Exception as e:
                    print(f"Lỗi khi xử lý nhà hàng: {e}")
            
            page += 1
            
            try:
                load_more_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.fd-btn-more"))
                )
                actions = ActionChains(driver)
                actions.move_to_element(load_more_button).perform()
                load_more_button.click()
                print(f"Đã chuyển sang trang {page + 1}")
                time.sleep(wait_time)
            except Exception as e:
                print(f"Không tìm thấy nút 'Xem thêm' hoặc đã hết trang: {e}")
                break        

    finally:
        driver.quit()
        print(f"Hoàn thành việc scrape hình ảnh! Đã xử lý {image_count} hình ảnh trên {page} trang.")
#-----------------------------------------------Excute------------------------------------
if __name__ == "__main__":
    # Gửi yêu cầu GET tới URL
    response = requests.get('https://www.foody.vn/')
    if response.status_code != 200:
        print(f"Không thể truy cập trang web. Mã trạng thái: {response.status_code}")
    chrome_options = Options()
    chrome_options.add_argument("--disable-images")    
    prefs = {"profile.managed_default_content_settings.images": 2}  # Tắt tải ảnh
    chrome_options.add_experimental_option("prefs", prefs)       
    # Tạo các tùy chọn Chrome nếu cần
    # Ví dụ: nếu bạn cần chạy Chrome dưới dạng headless (không hiển thị trình duyệt)
    # chrome_options.add_argument('--headless')
    # Phân tích HTML bằng BeautifulSoup
    # Lấy mã HTML của trang
    
    try:
        
        # Khởi tạo driver với Service thay cho executable_path
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https://www.foody.vn/')        
        # Đăng nhập 
        login('https://www.foody.vn/',"trantrongkhang0941@gmail.com", "0833030679")
        link_img = "https://www.foody.vn/"
        output_folder = "D:\DoAn_01\crawl_data\data\img_04"
        crawl_img = scrab_img(link_img,output_folder,5,100,5)
        #scrab = scrabing(max_pages=2,columns_name=['Rating', 'Name', 'Address'])
        # Lưu vào file Excel
        """excel_file = "foody_restaurants_04.xlsx"
        scrab.to_excel(excel_file, index=False, engine='openpyxl')
        print(f"Đã lưu dữ liệu vào file {excel_file}")"""

    except Exception as e:
        print(f"Lỗi xảy ra: {e}")

    finally:
        driver.quit()  # Đảm bảo trình duyệt được đóng đúng cách
    

    