from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

def build_model():
    # 1. Khởi tạo cấu trúc mạng: Lĩnh vực & Tháng ảnh hưởng trực tiếp đến tình trạng Quá tải
    model = BayesianNetwork([('LinhVuc', 'QuaTai'), ('Thang', 'QuaTai')])

    # 2. Thiết lập xác suất tiên nghiệm (Prior Probabilities)
    # Giả sử: 70% hồ sơ là Hộ tịch, 30% là Đất đai
    cpd_linhvuc = TabularCPD(variable='LinhVuc', variable_card=2, 
                             values=[[0.7], [0.3]], 
                             state_names={'LinhVuc': ['HoTich', 'DatDai']})
    
    # Giả sử: 60% là tháng bình thường, 40% là tháng cao điểm
    cpd_thang = TabularCPD(variable='Thang', variable_card=2, 
                           values=[[0.6], [0.4]], 
                           state_names={'Thang': ['BinhThuong', 'CaoDiem']})

    # 3. Bảng xác suất có điều kiện (CPD) cho biến "QuaTai"
    # Dữ liệu giả lập tỷ lệ ách tắc dựa trên sự kết hợp của Lĩnh vực và Tháng
    cpd_quatai = TabularCPD(
        variable='QuaTai', variable_card=2,
        values=[
            [0.9, 0.6, 0.5, 0.1], # Xác suất KHÔNG bị ách tắc (Bình thường)
            [0.1, 0.4, 0.5, 0.9]  # Xác suất CÓ bị ách tắc (Quá tải)
        ],
        evidence=['LinhVuc', 'Thang'],
        evidence_card=[2, 2],
        state_names={
            'QuaTai': ['Khong', 'Co'], 
            'LinhVuc': ['HoTich', 'DatDai'], 
            'Thang': ['BinhThuong', 'CaoDiem']
        }
    )

    model.add_cpds(cpd_linhvuc, cpd_thang, cpd_quatai)
    model.check_model() # Kiểm tra tính hợp lệ của mô hình
    return model

def predict_overload(linh_vuc, thang):
    model = build_model()
    infer = VariableElimination(model)
    # Thực hiện truy vấn để lấy xác suất xảy ra tình trạng "Có" quá tải
    result = infer.query(variables=['QuaTai'], evidence={'LinhVuc': linh_vuc, 'Thang': thang})
    return result.values[1] # Trả về giá trị tỷ lệ %