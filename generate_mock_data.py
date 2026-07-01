import pandas as pd
import numpy as np
import os

def generate_data(num_records=1000):
    np.random.seed(42) # Đảm bảo kết quả giống nhau ở mỗi lần sinh dữ liệu
    
    # Giả lập 70% hồ sơ Hộ tịch, 30% Đất đai
    linh_vuc = np.random.choice(['Hộ tịch / Chứng thực', 'Nhà ở / Đất đai'], size=num_records, p=[0.7, 0.3])
    
    # Giả lập 60% rơi vào tháng bình thường, 40% tháng cao điểm
    thang = np.random.choice(['Tháng thường', 'Tháng cao điểm'], size=num_records, p=[0.6, 0.4])
    
    # Tạo logic cho trạng thái hồ sơ (Quá tải/Trễ hẹn)
    trang_thai = []
    for lv, t in zip(linh_vuc, thang):
        if lv == 'Nhà ở / Đất đai' and t == 'Tháng cao điểm':
            # Nguy cơ trễ cực cao (90%)
            trang_thai.append(np.random.choice(['Đúng hạn', 'Trễ hẹn'], p=[0.1, 0.9]))
        elif lv == 'Nhà ở / Đất đai' or t == 'Tháng cao điểm':
            # Nguy cơ trung bình (50%)
            trang_thai.append(np.random.choice(['Đúng hạn', 'Trễ hẹn'], p=[0.5, 0.5]))
        else:
            # Nguy cơ thấp (10%)
            trang_thai.append(np.random.choice(['Đúng hạn', 'Trễ hẹn'], p=[0.9, 0.1]))
            
    # Tạo DataFrame
    df = pd.DataFrame({
        'Mã hồ sơ': [f'HS{str(i).zfill(5)}' for i in range(1, num_records + 1)],
        'Lĩnh vực': linh_vuc,
        'Thời điểm': thang,
        'Trạng thái': trang_thai
    })
    
    # Đảm bảo thư mục data/ tồn tại
    os.makedirs('data', exist_ok=True)
    
    # Xuất ra file CSV
    file_path = 'data/sample_phuong_saigon.csv'
    df.to_csv(file_path, index=False, encoding='utf-8-sig')
    print(f"✅ Đã tạo thành công {num_records} dòng dữ liệu tại: {file_path}")

if __name__ == "__main__":
    generate_data()