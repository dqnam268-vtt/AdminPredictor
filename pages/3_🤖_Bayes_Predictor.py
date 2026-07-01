import streamlit as st
import pandas as pd
from models.bayes_network import predict_overload
import plotly.express as px

st.header("🤖 Chẩn đoán & Dự báo Ách tắc")
st.write("Hệ thống ứng dụng mạng Xác suất Bayes để chẩn đoán rủi ro trễ hẹn.")

# Chia giao diện thành 2 Tabs
tab1, tab2 = st.tabs(["🔍 Chẩn đoán Từng trường hợp", "📂 Quét dữ liệu Hàng loạt (Batch)"])

# ==========================================
# TAB 1: CHẨN ĐOÁN CÁ NHÂN (Giữ nguyên như cũ)
# ==========================================
with tab1:
    st.subheader("Phân tích rủi ro cho hồ sơ đơn lẻ")
    with st.form("predict_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            linh_vuc = st.selectbox(
                "1. Lĩnh vực thủ tục:", 
                options=['Tư pháp - Hộ tịch', 'Tài nguyên - Môi trường', 'Lao động - Thương binh & Xã hội', 'Xây dựng', 'Kế hoạch - Đầu tư']
            )
        with col2:
            kenh = st.selectbox("2. Kênh nộp hồ sơ:", options=['Trực tuyến (DVC)', 'Trực tiếp tại quầy'])
        with col3:
            thang = st.selectbox("3. Tháng tiếp nhận:", options=[i for i in range(1, 13)], format_func=lambda x: f"Tháng {x}")
        
        submitted = st.form_submit_button("Tiến hành Chẩn đoán")

    if submitted:
        prob = predict_overload(linh_vuc, kenh, thang)
        percentage = prob * 100
        st.markdown("---")
        if percentage > 70:
            st.error(f"⚠️ Nguy cơ quá tải cực cao: {percentage:.1f}%")
        elif percentage > 40:
            st.warning(f"⚡ Nguy cơ chậm trễ trung bình: {percentage:.1f}%")
        else:
            st.success(f"✅ An toàn - Tỷ lệ quá tải thấp: {percentage:.1f}%")

# ==========================================
# TAB 2: CHẨN ĐOÁN HÀNG LOẠT (Tính năng mới)
# ==========================================
with tab2:
    st.subheader("Trí tuệ nhân tạo quét và phân loại rủi ro toàn bộ File")
    
    if 'current_data' not in st.session_state:
        st.warning("⚠️ Chưa có dữ liệu đầu vào. Vui lòng sang tab 'Tích hợp dữ liệu' để tải file lên.")
    else:
        df = st.session_state['current_data']
        st.info(f"Hệ thống đang lưu trữ **{len(df):,}** hồ sơ. Bấm nút bên dưới để quét toàn bộ.")
        
        if st.button("🚀 Kích hoạt AI Quét toàn bộ Dữ liệu", type="primary"):
            with st.spinner("Đang áp dụng thuật toán Bayes (Tối ưu hóa Lookup Table)..."):
                
                df_predict = df.copy()
                
                # Trích xuất tên cột tự động (dựa theo việc người dùng đã mapping ở trang Upload)
                linh_vuc_col = 'Lĩnh vực' if 'Lĩnh vực' in df_predict.columns else df_predict.columns[1]
                thang_col = 'Thời điểm' if 'Thời điểm' in df_predict.columns else df_predict.columns[2]
                kenh_col = 'Kênh nộp hồ sơ' if 'Kênh nộp hồ sơ' in df_predict.columns else None
                
                # 1. Tìm các tổ hợp độc nhất để tránh việc AI phải tính lại nhiều lần
                if kenh_col:
                    unique_combos = df_predict[[linh_vuc_col, kenh_col, thang_col]].drop_duplicates()
                else:
                    unique_combos = df_predict[[linh_vuc_col, thang_col]].drop_duplicates()
                
                # 2. Chạy thuật toán Bayes cho các tổ hợp này
                probs = []
                for _, row in unique_combos.iterrows():
                    lv = row[linh_vuc_col]
                    th = row[thang_col]
                    kn = row[kenh_col] if kenh_col else 'Trực tiếp tại quầy'
                    
                    # Tách lấy con số từ chuỗi tháng (VD: "Tháng 12" -> 12)
                    try:
                        th_val = int(''.join(filter(str.isdigit, str(th))))
                    except:
                        th_val = 1
                        
                    probs.append(predict_overload(lv, kn, th_val) * 100)
                
                unique_combos['Nguy cơ trễ hẹn (%)'] = probs
                
                # 3. Ghép (Map) kết quả xác suất trở lại bảng 10.000 dòng ban đầu
                df_result = pd.merge(df_predict, unique_combos, how='left')
                
                # Phân loại màu sắc
                def classify_risk(p):
                    if p > 70: return '🔴 Rủi ro Cao (>70%)'
                    elif p > 40: return '🟡 Rủi ro Trung bình'
                    else: return '🟢 An toàn (<40%)'
                
                df_result['Mức độ cảnh báo'] = df_result['Nguy cơ trễ hẹn (%)'].apply(classify_risk)
                
                # Vẽ biểu đồ tổng kết
                st.markdown("### 📊 Tổng quan Cảnh báo")
                risk_counts = df_result['Mức độ cảnh báo'].value_counts().reset_index()
                risk_counts.columns = ['Mức độ', 'Số lượng']
                
                fig = px.bar(
                    risk_counts, x='Mức độ', y='Số lượng', 
                    color='Mức độ',
                    color_discrete_map={
                        '🔴 Rủi ro Cao (>70%)': '#DC143C', 
                        '🟡 Rủi ro Trung bình': '#FFA500', 
                        '🟢 An toàn (<40%)': '#2E8B57'
                    }
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Hiển thị bảng dữ liệu có cảnh báo
                st.markdown("### 📋 Danh sách Hồ sơ kèm chẩn đoán AI")
                st.dataframe(
                    df_result.style.format({'Nguy cơ trễ hẹn (%)': "{:.1f}%"}), 
                    use_container_width=True
                )