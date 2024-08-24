import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Thiết lập Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument("--headless")  # Uncomment nếu bạn muốn chạy ở chế độ headless

# Khởi tạo WebDriver
driver = webdriver.Chrome(options=chrome_options)

# URL của trang web
url = "https://www.yelp.com/search?find_desc=Restaurants&find_loc=San+Francisco%2C+CA%2C+US"

# Hàm để scroll xuống cuối trang
def scroll_to_bottom():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# Hàm để crawl thông tin nhà hàng
def crawl_restaurants():
    restaurants = []
    try:
        # Đợi cho các phần tử nhà hàng xuất hiện
        restaurant_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.jemSU"))
        )
        
        for element in restaurant_elements:
            try:
                name = element.find_element(By.CSS_SELECTOR, "div.cBVir").text
                rating = element.find_element(By.CSS_SELECTOR, "svg.UctUV").get_attribute("aria-label")
                review_count = element.find_element(By.CSS_SELECTOR, "span.IiChw").text
                restaurants.append({
                    "name": name,
                    "rating": rating,
                    "review_count": review_count
                })
            except NoSuchElementException:
                continue
    except TimeoutException:
        print("Không thể tải các phần tử nhà hàng")
    
    return restaurants

# Truy cập trang web
driver.get(url)

# Danh sách để lưu tất cả các nhà hàng
all_restaurants = []

# Số trang muốn crawl
num_pages = 5

for page in range(num_pages):
    print(f"Đang crawl trang {page + 1}")
    
    # Crawl thông tin nhà hàng trên trang hiện tại
    restaurants = crawl_restaurants()
    all_restaurants.extend(restaurants)
    
    # Scroll xuống cuối trang
    scroll_to_bottom()
    
    # Tìm và click vào nút "Tiếp"
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.nav.next"))
        )
        next_button.click()
        time.sleep(random.uniform(2, 4))  # Đợi trang mới tải
    except TimeoutException:
        print("Không tìm thấy nút 'Tiếp' hoặc đã đến trang cuối cùng")
        break

# In kết quả
for restaurant in all_restaurants:
    print(f"Tên: {restaurant['name']}")
    print(f"Đánh giá: {restaurant['rating']}")
    print(f"Số đánh giá: {restaurant['review_count']}")
    print("--------------------")

# Đóng trình duyệt
driver.quit()

print(f"Tổng số nhà hàng đã crawl: {len(all_restaurants)}")