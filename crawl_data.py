# -*- coding: utf-8 -*-
#------------ ĐOẠN 1--------------------------------
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, StaleElementReferenceException,NoSuchElementException
import pandas as pd
from bs4 import BeautifulSoup
import requests

# Gửi yêu cầu GET tới URL
response = requests.get('https://www.foody.vn/')
if response.status_code != 200:
    print(f"Không thể truy cập trang web. Mã trạng thái: {response.status_code}")
        

# Phân tích nội dung HTML
driver = webdriver.Chrome()
driver.get('https://www.foody.vn/')

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

def crawl_restaurants_on_page():

    # Tìm các phần tử sau khi JavaScript đã tải xong
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')    

    # Tìm tất cả các phần tử chứa thông tin nhà hàng
    restaurant_items = soup.find_all('div', class_='content-item ng-scope')
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
#-----------------------------------------Main-----------------------------------------
# Đăng nhập 
login('https://www.foody.vn/',"trantrongkhang0941@gmail.com", "0833030679")

# load trang để tiến hành crawl
all_data = []
i = 0
max_attempts = 3
max_pages = 10  # Số trang tối đa bạn muốn crawl
while i < max_pages:
    close_popups()
    
    # Crawl dữ liệu trên trang hiện tại
    page_data = crawl_restaurants_on_page()
    all_data.extend(page_data)
    print(f"Đã crawl {len(page_data)} nhà hàng từ trang {i+1}")
    success = False
    for attempt in range(max_attempts):
        if click_load_more():
            success = True
            break
        else:
            print(f"Không thể click 'Xem thêm' lần thứ {i+1}. Thử lại lần {attempt+1}/{max_attempts}")
            time.sleep(2)
    
    if success:
        i += 1
        print(f"Đã chuyển sang trang {i+1}")
    else:
        print(f"Không thể click 'Xem thêm' sau {max_attempts} lần thử. Dừng crawl.")
        break

    time.sleep(random.uniform(1, 2))



#-------------------------------lưu kết quả--------------------------------------
# Tạo DataFrame từ dữ liệu đã crawl
df = pd.DataFrame(page_data, columns=['Rating', 'Name', 'Address'])
# Debug: In ra 5 dòng đầu tiên của dữ liệu
print(df.head())
# Lưu vào file Excel
excel_file = "foody_restaurants_03.xlsx"
df.to_excel(excel_file, index=False, engine='openpyxl')
print(f"Đã lưu dữ liệu vào file {excel_file}")

driver.quit()
