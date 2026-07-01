from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

def build_model():
    # Thêm biến 'Kenh' (Kênh tiếp nhận) vào mạng lưới để phân tích sâu hơn
    model = BayesianNetwork([('LinhVuc', 'QuaTai'), ('Kenh', 'QuaTai'), ('Thang', 'QuaTai')])

    # 1. Nhóm Lĩnh vực: Phân loại thành Cơ bản (Hộ tịch, LĐTBXH, KHĐT) và Phức tạp (Tài nguyên, Xây dựng)
    cpd_linhvuc = TabularCPD(variable='LinhVuc', variable_card=2, 
                             values=[[0.65], [0.35]], 
                             state_names={'LinhVuc': ['CoBan', 'PhucTap']})
    
    # 2. Nhóm Kênh nộp: Trực tuyến và Trực tiếp
    cpd_kenh = TabularCPD(variable='Kenh', variable_card=2, 
                          values=[[0.6], [0.4]], 
                          state_names={'Kenh': ['TrucTuyen', 'TrucTiep']})

    # 3. Nhóm Tháng: Bình thường và Cao điểm (Lễ/Tết)
    cpd_thang = TabularCPD(variable='Thang', variable_card=2, 
                           values=[[0.58], [0.42]], 
                           state_names={'Thang': ['BinhThuong', 'CaoDiem']})

    # 4. Bảng Xác suất có điều kiện (CPD) kết hợp 3 biến số đầu vào
    cpd_quatai = TabularCPD(
        variable='QuaTai', variable_card=2,
        values=[
            # Xác suất KHÔNG trễ hẹn (Tỷ lệ nghịch với độ khó)
            [0.95, 0.75, 0.80, 0.60, 0.65, 0.45, 0.50, 0.10],
            # Xác suất CÓ trễ hẹn
            [0.05, 0.25, 0.20, 0.40, 0.35, 0.55, 0.50, 0.90]
        ],
        evidence=['LinhVuc', 'Kenh', 'Thang'],
        evidence_card=[2, 2, 2],
        state_names={
            'QuaTai': ['Khong', 'Co'], 
            'LinhVuc': ['CoBan', 'PhucTap'], 
            'Kenh': ['TrucTuyen', 'TrucTiep'],
            'Thang': ['BinhThuong', 'CaoDiem']
        }
    )

    model.add_cpds(cpd_linhvuc, cpd_kenh, cpd_thang, cpd_quatai)
    model.check_model()
    return model

def predict_overload(linh_vuc_raw, kenh_raw, thang_raw):
    # Ánh xạ dữ liệu thực tế từ UI vào các nhóm của thuật toán Bayes
    linh_vuc = 'PhucTap' if linh_vuc_raw in ['Tài nguyên - Môi trường', 'Xây dựng'] else 'CoBan'
    kenh = 'TrucTiep' if kenh_raw == 'Trực tiếp tại quầy' else 'TrucTuyen'
    thang = 'CaoDiem' if thang_raw in [2, 3, 10, 11, 12] else 'BinhThuong'

    model = build_model()
    infer = VariableElimination(model)
    result = infer.query(variables=['QuaTai'], evidence={'LinhVuc': linh_vuc, 'Kenh': kenh, 'Thang': thang})
    
    return result.values[1] # Trả về % tỷ lệ trễ hẹn (Quá tải = Có)