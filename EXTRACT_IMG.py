from PIL import Image
import pytesseract
import os

# Đường dẫn đến tesseract.exe nếu bạn sử dụng Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def convert_images_in_folder_to_texts(folder_path, output_dir):
    """
    Hàm chuyển đổi tất cả file ảnh trong một thư mục thành các file văn bản sử dụng Tesseract OCR.

    Args:
    - folder_path (str): Đường dẫn đến thư mục chứa các file hình ảnh.
    - output_dir (str): Đường dẫn đến thư mục lưu trữ file văn bản đầu ra.

    Returns:
    - None
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Duyệt qua tất cả các file trong thư mục
    for file_name in os.listdir(folder_path):
        # Tạo đường dẫn đầy đủ đến file
        file_path = os.path.join(folder_path, file_name)
        
        # Kiểm tra nếu file là ảnh (jpg, jpeg, png)
        if os.path.isfile(file_path) and file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
            try:
                # Mở hình ảnh sử dụng Pillow
                img = Image.open(file_path)
                
                # Sử dụng Tesseract OCR để chuyển đổi hình ảnh thành văn bản
                text = pytesseract.image_to_string(img, lang='eng')  # 'lang' có thể đổi sang ngôn ngữ khác nếu cần

                # Lấy tên file không có phần mở rộng để tạo tên file đầu ra
                base_name = os.path.splitext(file_name)[0]
                
                # Tạo đường dẫn file đầu ra
                output_text_path = os.path.join(output_dir, f"{base_name}.txt")
                
                # Lưu văn bản vào file .txt
                with open(output_text_path, 'w', encoding='utf-8') as text_file:
                    text_file.write(text)

                print(f"Đã chuyển đổi thành công {file_path} sang {output_text_path}")
            except Exception as e:
                print(f"Lỗi khi chuyển đổi hình ảnh {file_path} thành văn bản: {e}")

# Ví dụ sử dụng hàm với thư mục chứa hình ảnh
folder_path = r'C:\Users\Admin\Pictures\Saved Pictures\nlp_LAB3'  # Thay đổi đường dẫn đến thư mục chứa hình ảnh của bạn

# Thư mục lưu trữ file văn bản đầu ra
output_dir = r'D:\_extract\NLP_lab3'

# Gọi hàm để chuyển đổi tất cả ảnh trong thư mục thành các file văn bản
convert_images_in_folder_to_texts(folder_path, output_dir)
