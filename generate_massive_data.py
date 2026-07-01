import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_massive_dataset(num_records=10000):
    np.random.seed(2026) # Cố định seed cho năm 2026
    
    # 1. Các lĩnh vực hành chính đa dạng tại cấp Phường/Quận
    danh_sach_linh_vuc = [
        'Tư pháp - Hộ tịch', 
        'Tài nguyên - Môi trường', 
        'Lao động - Thương binh & Xã hội', 
        'Xây dựng', 
        'Kế hoạch - Đầu tư'
    ]
    ty_trong_linh_vuc = [0.4, 0.25, 0.15, 0.1, 0.1] # Hộ tịch và Đất đai luôn chiếm đa số
    
    linh_vuc_data = np.random.choice(danh_sach_linh_vuc, size=num_records, p=ty_trong_linh_vuc)
    
    # 2. Kênh tiếp nhận (Thêm biến số về Chuyển đổi số)
    kenh_tiep_nhan = np.random.choice(['Trực tuyến (DVC)', 'Trực tiếp tại quầy'], size=num_records, p=[0.6, 0.4])
    
    # 3. Tháng tiếp nhận (Mô phỏng cả năm)
    thang_tiep_nhan = np.random.randint(1, 13, size=num_records)
    
    # 4. Logic tạo Trạng thái hồ sơ phức tạp và thực tế hơn
    trang_thai = []
    thoi_gian_xu_ly = [] # Tính bằng ngày
    
    for lv, kenh, thang in zip(linh_vuc_data, kenh_tiep_nhan, thang_tiep_nhan):
        # Thiết lập các điều kiện làm tăng nguy cơ trễ hẹn
        nguy_co_tre = 0.05 # Mức cơ bản 5%
        
        # Đất đai và Xây dựng phức tạp hơn, dễ trễ hơn
        if lv in ['Tài nguyên - Môi trường', 'Xây dựng']:
            nguy_co_tre += 0.3
            
        # Nộp trực tiếp mất thời gian xử lý giấy tờ hơn trực tuyến
        if kenh == 'Trực tiếp tại quầy':
            nguy_co_tre += 0.15
            
        # Các tháng cuối năm (10, 11, 12) hoặc sau Tết (tháng 2, 3) thường quá tải
        if thang in [2, 3, 10, 11, 12]:
            nguy_co_tre += 0.2
            
        # Chốt trạng thái dựa trên xác suất nguy cơ
        if np.random.rand() < nguy_co_tre:
            trang_thai.append('Trễ hẹn')
            thoi_gian_xu_ly.append(np.random.randint(15, 45)) # Trễ thì tốn nhiều ngày hơn
        else:
            trang_thai.append('Đúng hạn')
            thoi_gian_xu_ly.append(np.random.randint(1, 14)) # Xử lý nhanh
            
    # 5. Đóng gói thành DataFrame với tên cột chuẩn hóa theo Cổng DVC
    df = pd.DataFrame({
        'Mã hồ sơ': [f'DVC-{2026}-{str(i).zfill(6)}' for i in range(1, num_records + 1)],
        'Nhóm lĩnh vực': linh_vuc_data,
        'Kênh nộp hồ sơ': kenh_tiep_nhan,
        'Tháng phát sinh': [f'Tháng {t}' for t in thang_tiep_nhan],
        'Số ngày giải quyết': thoi_gian_xu_ly,
        'Kết quả đánh giá': trang_thai
    })
    
    # Đảm bảo thư mục lưu trữ tồn tại
    os.makedirs('data', exist_ok=True)
    file_path = 'data/du_lieu_hanh_chinh_tong_quat.csv'
    
    # Trộn ngẫu nhiên các hàng để dữ liệu trông tự nhiên
    df = df.sample(frac=1).reset_index(drop=True)
    
    df.to_csv(file_path, index=False, encoding='utf-8-sig')
    print(f"✅ Đã tạo thành công {num_records} hồ sơ tổng quát tại: {file_path}")

if __name__ == "__main__":
    generate_massive_dataset()