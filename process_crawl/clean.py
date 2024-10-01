import os
import pandas as pd
from fuzzywuzzy import fuzz
import shutil

def find_best_match(target, choices):
    return max(choices, key=lambda x: fuzz.ratio(target, x))

# Đường dẫn tới folder chứa ảnh gốc và file CSV
folder_path = r'D:\DoAn_01\crawl_data\data\img_02'
csv_path = r'D:\DoAn_01\crawl_data\data\clean_data_01.csv'
temp_folder = r'D:\DoAn_01\crawl_data\data\img_01'

# Kiểm tra và tạo thư mục tạm thời
if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)

# Kiểm tra xem thư mục và file CSV có tồn tại không
if not os.path.exists(folder_path):
    print(f"Thư mục {folder_path} không tồn tại.")
    exit()

if not os.path.exists(csv_path):
    print(f"File CSV {csv_path} không tồn tại.")
    exit()

# Đọc file CSV
try:
    df = pd.read_csv(csv_path)
except Exception as e:
    print(f"Lỗi khi đọc file CSV: {e}")
    exit()

# Drop các hàng dư thừa sao cho chỉ còn 890 hàng
df = df.iloc[:890]  # Giữ lại 890 hàng đầu tiên

success_count = 0
error_count = 0

# Lấy danh sách tất cả các file trong thư mục
all_files = os.listdir(folder_path)

print(f"Tổng số file cần xử lý: {len(df)}")

# Đổi tên file
for index, row in df.iterrows():
    new_name = row['image_path']
    if not new_name.lower().endswith('.jpg'):
        new_name += '.jpg'
    
    # Tìm file gốc có tên gần giống nhất
    old_name = find_best_match(new_name, all_files)

    old_path = os.path.join(folder_path, old_name)
    temp_path = os.path.join(temp_folder, new_name)

    print(f"\nĐang xử lý file {index+1}/{len(df)}:")
    print(f"Tên cũ: {old_path}")
    print(f"Tên mới (tạm thời): {temp_path}")

    if os.path.exists(old_path):
        try:
            shutil.copy2(old_path, temp_path)
            print("Sao chép thành công")
            success_count += 1
        except Exception as e:
            print(f"Lỗi khi sao chép: {e}")
            error_count += 1
    else:
        print(f"File gốc không tồn tại: {old_path}")
        error_count += 1

    if (index + 1) % 100 == 0:
        print(f"\nTiến độ: {index + 1}/{len(df)} files")
        print(f"Số file đã sao chép thành công: {success_count}")
        print(f"Số file gặp lỗi: {error_count}")

# Di chuyển tất cả các file từ thư mục tạm thời về thư mục gốc
print("\nĐang di chuyển các file đã đổi tên về thư mục gốc...")
for filename in os.listdir(temp_folder):
    src = os.path.join(temp_folder, filename)
    dst = os.path.join(folder_path, filename)
    try:
        shutil.move(src, dst)
    except Exception as e:
        print(f"Lỗi khi di chuyển file {filename}: {e}")

# Xóa thư mục tạm thời
shutil.rmtree(temp_folder)

print(f"\nKết quả cuối cùng:")
print(f"Số file đã đổi tên thành công: {success_count}")
print(f"Số file gặp lỗi: {error_count}")