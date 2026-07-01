import streamlit as st
import plotly.express as px

st.header("📊 Bảng điều khiển Thống kê Hành chính")
st.markdown("---")

# Kiểm tra xem người dùng đã tải dữ liệu lên chưa
if 'current_data' not in st.session_state:
    st.warning("⚠️ Chưa có dữ liệu đầu vào. Vui lòng sang tab 'Tích hợp dữ liệu' để tải file CSV lên trước.")
else:
    df = st.session_state['current_data']
    
    # Tính toán các chỉ số tổng quan (KPIs)
    tong_ho_so = len(df)
    so_tre_hen = len(df[df['Trạng thái'] == 'Trễ hẹn'])
    ty_le_tre = (so_tre_hen / tong_ho_so) * 100
    
    # Hiển thị thẻ KPI
    col1, col2, col3 = st.columns(3)
    col1.metric("Tổng số hồ sơ tiếp nhận", f"{tong_ho_so:,}")
    col2.metric("Hồ sơ trễ hẹn", f"{so_tre_hen:,}")
    col3.metric("Tỷ lệ trễ hẹn", f"{ty_le_tre:.2f}%", delta=f"{ty_le_tre-5:.2f}% (so với mục tiêu)", delta_color="inverse")
    
    st.markdown("---")
    
    # Vẽ biểu đồ bằng Plotly
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Cơ cấu Lĩnh vực thủ tục")
        fig_pie = px.pie(df, names='Lĩnh vực', hole=0.4, color_discrete_sequence=px.colors.sequential.Teal)
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col_chart2:
        st.subheader("Tình trạng Trễ hẹn theo Lĩnh vực")
        fig_bar = px.histogram(
            df, x='Lĩnh vực', color='Trạng thái', 
            barmode='group',
            color_discrete_map={'Đúng hạn': '#2E8B57', 'Trễ hẹn': '#DC143C'}
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
    st.info("💡 Hệ thống ghi nhận tỷ lệ trễ hẹn có dấu hiệu tăng cục bộ. Khuyến nghị chuyển sang tab **🤖 Chẩn đoán & Dự báo** để phân tích nguyên nhân bằng thuật toán Bayes.")