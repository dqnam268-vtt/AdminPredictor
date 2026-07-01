import streamlit as st
import pandas as pd

st.header("📤 Tích hợp & Chuẩn hóa dữ liệu")
st.write("Tải lên file báo cáo thống kê (CSV) được trích xuất từ hệ thống một cửa điện tử.")

uploaded_file = st.file_uploader("Chọn file CSV dữ liệu hồ sơ", type=['csv'])

if uploaded_file is not None:
    try:
        # Đọc file dữ liệu thô
        df_raw = pd.read_csv(uploaded_file)
        st.success("Tải dữ liệu thành công! Vui lòng thực hiện chuẩn hóa bên dưới.")
        
        # Lấy danh sách tên các cột có trong file vừa tải lên
        available_columns = df_raw.columns.tolist()
        
        st.markdown("### ⚙️ Ghép nối (Mapping) Cấu trúc Dữ liệu")
        st.info("Hệ thống nhận thấy cấu trúc file có thể khác biệt. Vui lòng chọn các cột tương ứng để hệ thống hiểu dữ liệu của bạn.")
        
        # Tạo giao diện để cán bộ tự chỉ định cột
        col1, col2 = st.columns(2)
        with col1:
            col_linhvuc = st.selectbox("1. Cột nào chứa dữ liệu 'Lĩnh vực thủ tục'?", available_columns)
            col_thoidiem = st.selectbox("2. Cột nào chứa dữ liệu 'Thời điểm/Tháng'?", available_columns)
        with col2:
            col_trangthai = st.selectbox("3. Cột nào chứa dữ liệu 'Trạng thái (Đúng hạn/Trễ hẹn)'?", available_columns)
            
        if st.button("Xác nhận Chuẩn hóa"):
            # Đổi tên cột của file tải lên thành chuẩn chung của hệ thống
            df_standard = df_raw.rename(columns={
                col_linhvuc: 'Lĩnh vực',
                col_thoidiem: 'Thời điểm',
                col_trangthai: 'Trạng thái'
            })
            
            # Lưu dữ liệu ĐÃ CHUẨN HÓA vào bộ nhớ để các trang khác sử dụng
            st.session_state['current_data'] = df_standard
            
            st.success("✅ Chuẩn hóa thành công! Hệ thống đã hiểu cấu trúc dữ liệu của bạn.")
            st.dataframe(df_standard.head()) # Hiển thị 5 dòng sau chuẩn hóa để kiểm tra
            st.write("💡 Hãy chuyển sang tab **Dashboard** hoặc **Chẩn đoán & Dự báo** để xem kết quả.")
            
    except Exception as e:
        st.error(f"Có lỗi xảy ra trong quá trình xử lý file: {e}")
else:
    st.warning("Vui lòng tải lên file dữ liệu để tiếp tục.")