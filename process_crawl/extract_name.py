import os
import csv

def update_csv_with_image_paths(img_folder, csv_file):
    # Lấy danh sách tất cả các file trong thư mục img
    image_files = [f for f in os.listdir(img_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    
    # Đọc file CSV hiện có
    rows = []
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    
    # Cập nhật cột [image_path]
    for i, row in enumerate(rows):
        if i < len(image_files):
            image_name = os.path.splitext(image_files[i])[0]  # Lấy tên file không có phần mở rộng
            row['image_path_02'] = f'images/{image_name}.jpg'
        else:
            row['image_path_02'] = ''  # Nếu hết ảnh, để trống
    
    # Ghi lại vào file CSV
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        fieldnames = rows[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

# Sử dụng hàm
update_csv_with_image_paths(r'D:\DoAn_01\crawl_data\data\img', r'D:\DoAn_01\crawl_data\data\restaurant_info.csv')