import matplotlib.pyplot as plt # Nhập thư viện matplotlib.pyplot để vẽ biểu đồ, sử dụng alias là plt cho tiện lợi.
from scipy import stats # Nhập module stats từ thư viện scipy, chứa các hàm thống kê.

# Tính toán đường hồi quy
slope, intercept, r_value, p_value, std_err = stats.linregress(df_grouped['DATE OCC'].astype('int64'), df_grouped['LOCATION']) 
# Sử dụng hàm linregress từ module stats để tính toán đường hồi quy tuyến tính giữa 'DATE OCC' và 'LOCATION'.
# Chuyển đổi 'DATE OCC' sang kiểu int64 để phù hợp với hàm linregress.
# Kết quả trả về các giá trị: độ dốc (slope), hệ số chặn (intercept), hệ số tương quan (r_value), giá trị p (p_value), và sai số chuẩn (std_err).

# Vẽ biểu đồ scatter
plt.scatter(df_grouped['DATE OCC'], df_grouped['LOCATION'], s=50, alpha=0.7) 
# Vẽ biểu đồ scatter với 'DATE OCC' trên trục x và 'LOCATION' trên trục y.
# s=50: kích thước của các điểm.
# alpha=0.7: độ trong suốt của các điểm.

# Vẽ đường hồi quy
plt.plot(df_grouped['DATE OCC'], intercept + slope * df_grouped['DATE OCC'].astype('int64'), color='red') 
# Vẽ đường hồi quy dựa trên các giá trị đã tính toán.
# color='red': màu của đường hồi quy.

# Tùy chỉnh biểu đồ
plt.xlabel('DATE OCC') # Đặt nhãn cho trục x.
plt.ylabel('LOCATION') # Đặt nhãn cho trục y.
plt.title('Biểu đồ Scatter với Đường Hồi quy') # Đặt tiêu đề cho biểu đồ.
plt.grid(True) # Hiển thị lưới trên biểu đồ.
plt.show() # Hiển thị biểu đồ.
