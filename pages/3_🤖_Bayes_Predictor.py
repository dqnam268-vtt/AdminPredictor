import streamlit as st
from models.bayes_network import predict_overload

st.header("🤖 Chẩn đoán & Dự báo Ách tắc (Bản Tổng quát)")
st.write("Công cụ ứng dụng mạng Xác suất Bayes để chẩn đoán nguy cơ trễ hẹn dựa trên hệ thống dữ liệu hành chính quy mô lớn.")

# Tạo form nhập liệu cho cán bộ với 3 cột
with st.form("predict_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        linh_vuc = st.selectbox(
            "1. Lĩnh vực thủ tục:", 
            options=[
                'Tư pháp - Hộ tịch', 
                'Tài nguyên - Môi trường', 
                'Lao động - Thương binh & Xã hội', 
                'Xây dựng', 
                'Kế hoạch - Đầu tư'
            ]
        )
    with col2:
        kenh = st.selectbox(
            "2. Kênh nộp hồ sơ:", 
            options=['Trực tuyến (DVC)', 'Trực tiếp tại quầy']
        )
    with col3:
        thang = st.selectbox(
            "3. Tháng tiếp nhận:", 
            options=[i for i in range(1, 13)],
            format_func=lambda x: f"Tháng {x}"
        )
    
    submitted = st.form_submit_button("Tiến hành Chẩn đoán bằng AI")

if submitted:
    prob = predict_overload(linh_vuc, kenh, thang)
    percentage = prob * 100
    
    st.markdown("---")
    st.subheader("📊 Kết quả dự báo:")
    
    if percentage > 70:
        st.error(f"⚠️ Nguy cơ quá tải cực cao: {percentage:.1f}%")
        st.write("**Khuyến nghị:** Đề nghị Lãnh đạo điều động thêm nhân sự. Nếu là hồ sơ nộp trực tiếp, cần ưu tiên hướng dẫn người dân tạo tài khoản nộp trực tuyến để giảm tải quy trình giấy.")
    elif percentage > 40:
        st.warning(f"⚡ Nguy cơ chậm trễ trung bình: {percentage:.1f}%")
        st.write("**Khuyến nghị:** Theo dõi sát sao tiến độ luân chuyển hồ sơ nội bộ, đặc biệt là sự phối hợp giữa bộ phận Một cửa và bộ phận chuyên môn.")
    else:
        st.success(f"✅ An toàn - Tỷ lệ quá tải thấp: {percentage:.1f}%")
        st.write("**Đánh giá:** Nguồn lực hiện tại đang đáp ứng tốt nhu cầu của người dân.")