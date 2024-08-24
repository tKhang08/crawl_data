import requests
from bs4 import BeautifulSoup
import pandas as pd
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from selenium import webdriver
# Hàm crawl dữ liệu cho tất cả các nhà hàng trên một trang
def crawl_restaurants_on_page(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Không thể truy cập trang web. Mã trạng thái: {response.status_code}")
        return []

    driver = webdriver.Chrome()
    driver.get(url)

    # Tìm các phần tử sau khi JavaScript đã tải xong
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')    

    # Tìm tất cả các phần tử chứa thông tin nhà hàng
    restaurant_items = soup.find_all('div', class_='content-item ng-scope')
    restaurants_data = []

    for item in restaurant_items:
        # Tìm rating
        rating_tag = item.find('div', class_='review-points green')
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

# Crawl dữ liệu từ trang web
url = 'https://www.foody.vn/'
restaurants_data = crawl_restaurants_on_page(url)

# Chuyển dữ liệu thành DataFrame Pandas
df = pd.DataFrame(restaurants_data, columns=['Rating', 'Name', 'Address'])

# Lưu DataFrame vào file Excel
excel_file = 'restaurants_data.xlsx'
df.to_excel(excel_file, index=False)
print(f"Đã lưu dữ liệu vào file {excel_file}")

# Xác thực và tải file lên Google Drive
def upload_to_google_drive(file_path):
    # Xác thực với Google
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    # Tạo và tải file lên Google Drive
    file_drive = drive.CreateFile({'title': file_path})
    file_drive.SetContentFile(file_path)
    file_drive.Upload()
    print(f"Đã tải lên Google Drive với ID: {file_drive['id']}")

# Tải file Excel lên Google Drive
#upload_to_google_drive(excel_file)
