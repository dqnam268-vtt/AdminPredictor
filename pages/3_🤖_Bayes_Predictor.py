import streamlit as st
from models.bayes_network import predict_overload

st.header("🤖 Chẩn đoán và Dự báo Ách tắc")
st.write("Công cụ ứng dụng Xác suất Bayes để dự báo nguy cơ trễ hẹn hồ sơ dựa trên các tham số đầu vào.")

# Tạo form nhập liệu cho cán bộ
with st.form("predict_form"):
    col1, col2 = st.columns(2)
    with col1:
        linh_vuc = st.selectbox(
            "Chọn Lĩnh vực thủ tục:", 
            options=["HoTich", "DatDai"], 
            format_func=lambda x: "Hộ tịch / Chứng thực" if x == "HoTich" else "Nhà ở / Đất đai"
        )
    with col2:
        thang = st.selectbox(
            "Thời điểm xử lý:", 
            options=["BinhThuong", "CaoDiem"],
            format_func=lambda x: "Tháng thường" if x == "BinhThuong" else "Tháng cao điểm (Lễ/Cuối năm)"
        )
    
    submitted = st.form_submit_button("Tiến hành Chẩn đoán")

if submitted:
    prob = predict_overload(linh_vuc, thang)
    percentage = prob * 100
    
    st.markdown("---")
    st.subheader("📊 Kết quả dự báo:")
    
    # Giao diện cảnh báo theo mức độ phần trăm
    if percentage > 70:
        st.error(f"⚠️ Nguy cơ quá tải cực cao: {percentage:.1f}%")
        st.write("**Khuyến nghị:** Đề nghị Lãnh đạo điều động thêm ít nhất 01 nhân sự tăng cường cho quầy giải quyết lĩnh vực này.")
    elif percentage > 40:
        st.warning(f"⚡ Nguy cơ chậm trễ trung bình: {percentage:.1f}%")
        st.write("**Khuyến nghị:** Theo dõi sát sao tiến độ luân chuyển hồ sơ nội bộ.")
    else:
        st.success(f"✅ An toàn - Tỷ lệ quá tải thấp: {percentage:.1f}%")
        st.write("**Đánh giá:** Nguồn lực hiện tại đang đáp ứng tốt nhu cầu của người dân.")