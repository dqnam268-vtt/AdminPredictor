import streamlit as st
import pandas as pd

st.header("📤 Tích hợp dữ liệu Cổng Dịch vụ công")
st.write("Tải lên file báo cáo thống kê (CSV) được trích xuất từ hệ thống một cửa điện tử.")

uploaded_file = st.file_uploader("Chọn file CSV dữ liệu hồ sơ", type=['csv'])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("Tải dữ liệu thành công! Trích xuất 5 dòng đầu tiên:")
        st.dataframe(df.head())
        
        # Lưu dataframe vào session_state để trang Dashboard có thể đọc và vẽ biểu đồ
        st.session_state['current_data'] = df
        
        st.info("💡 Hãy chuyển sang tab 'Dashboard' để xem biểu đồ thống kê chi tiết.")
    except Exception as e:
        st.error(f"Có lỗi xảy ra khi đọc file: {e}")
else:
    st.warning("Vui lòng tải lên file dữ liệu mẫu để tiếp tục.")