import streamlit as st

# Cấu hình toàn cục cho ứng dụng
st.set_page_config(
    page_title="AdminPredictor - Phường Sài Gòn", 
    page_icon="🏛️", 
    layout="wide"
)

st.title("🏛️ AdminPredictor: Hệ thống Dự báo Hành chính")
st.markdown("---")

st.markdown("""
### Chào mừng Ban Giám khảo đến với không gian trải nghiệm AdminPredictor!
Giải pháp này được phát triển nhằm hưởng ứng **Hội thi đổi mới, sáng tạo về cải cách hành chính năm 2026 của Phường Sài Gòn**.

**Mục tiêu cốt lõi:**
* 📊 **Số hóa:** Chuyển đổi dữ liệu thống kê thụ động thành các biểu đồ trực quan.
* 🤖 **Dự báo (Xác suất Bayes):** Tính toán và chẩn đoán trước các điểm nghẽn tại bộ phận một cửa.
* ⚡ **Chủ động:** Hỗ trợ Lãnh đạo Ủy ban ra quyết định điều phối nhân sự kịp thời, giảm thiểu tỷ lệ trễ hẹn.

👈 *Vui lòng chọn các tính năng ở thanh điều hướng (Sidebar) bên trái để trải nghiệm.*
""")