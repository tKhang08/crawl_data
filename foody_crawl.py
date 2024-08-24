import logging
import pandas as pd
from model import *
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Crawl dữ liệu
data = crawl_foody('https://www.foody.vn/',max_pages=10)

# In ra số lượng nhà hàng đã crawl
print(f'Tổng số nhà hàng đã crawl: {len(data)}')
# Tạo DataFrame
df = pd.DataFrame(data)

# Lưu vào file Excel
if not df.empty:
    excel_file = 'foody_restaurants_names.xlsx'
    df.to_excel(excel_file, index=False)
    logging.info(f'Dữ liệu đã được lưu vào {excel_file}')

# In ra 5 dòng đầu tiên của dữ liệu
print(df.head())

# In ra tổng số nhà hàng đã crawl
print(f'Tổng số nhà hàng đã crawl: {len(df)}')