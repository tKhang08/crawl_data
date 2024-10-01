import os
import requests

# Thông tin GitHub của bạn
GITHUB_USERNAME = 'your_github_username'
GITHUB_TOKEN = 'your_github_token'  # Personal Access Token
REPO_NAME = 'your_new_repo_name'

# Bước 1: Tạo repository mới trên GitHub
def create_github_repo():
    url = 'https://api.github.com/user/repos'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        'name': REPO_NAME,
        'private': False  # Thay đổi thành True nếu bạn muốn repo riêng tư
    }
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        print(f"Repository '{REPO_NAME}' created successfully on GitHub.")
    else:
        print(f"Failed to create repository. Status code: {response.status_code}")
        print(response.json())

# Bước 2: Khởi tạo Git repository trong folder hiện tại và đẩy lên GitHub
def initialize_git_repo():
    os.system('git init')  # Khởi tạo repository Git cục bộ
    os.system('git add .')  # Thêm tất cả file vào staging area
    os.system('git commit -m "Initial commit"')  # Tạo commit đầu tiên
    os.system(f'git remote add origin https://github.com/{GITHUB_USERNAME}/{REPO_NAME}.git')  # Thêm remote GitHub
    os.system('git branch -M main')  # Đổi tên nhánh chính thành main 
    os.system('git push -u origin main')  # Đẩy code lên GitHub


create_github_repo()
initialize_git_repo()
