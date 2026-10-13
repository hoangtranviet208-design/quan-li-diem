import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Quản lý điểm sinh viên", layout="centered")

# ---------- Dữ liệu ----------
@st.cache_data
def tao_du_lieu():
    df = pd.DataFrame({
        "Ho_ten": ["Nguyễn Văn An", "Trần Thị Bình", "Lê Minh Chi", "Phạm Quốc Dũng", "Hoàng Thu Hà",
                   "Vũ Ngọc Lan", "Đặng Quang Minh", "Bùi Hải Nam", "Ngô Gia Phúc", "Đỗ Thùy Trang"],
        "Chuyen_can": [9, 8, 7, 10, 8, 6, 9, 7, 8, 10],
        "Giua_ky": [7.5, 8, 6, 9, 7, 5.5, 8.5, 6.5, 7, 9],
        "Cuoi_ky": [8, 8.5, 6.5, 9.5, 7, 5.5, 9, 7, 7.5, 9.5],
    })
    df["Tong_ket"] = (0.2 * df["Chuyen_can"] + 0.3 * df["Giua_ky"] + 0.5 * df["Cuoi_ky"]).round(2)
    df["Xep_loai"] = pd.cut(df["Tong_ket"], bins=[-float("inf"), 5, 7, 8.5, float("inf")],
                            labels=["Yếu", "Trung bình", "Khá", "Giỏi"], right=False).astype(str)
    return df

df = tao_du_lieu()

# ---------- Giao diện ----------
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

st.subheader("Bảng điểm")
bang = df.rename(columns={"Ho_ten": "Họ tên", "Chuyen_can": "Chuyên cần", "Giua_ky": "Giữa kỳ",
                          "Cuoi_ky": "Cuối kỳ", "Tong_ket": "Tổng kết", "Xep_loai": "Xếp loại"})
st.dataframe(bang, use_container_width=True, hide_index=True)

st.subheader("Thống kê")
cao = df.loc[df["Tong_ket"].idxmax()]
thap = df.loc[df["Tong_ket"].idxmin()]
c1, c2 = st.columns(2)
c1.metric("Điểm trung bình lớp", f"{df['Tong_ket'].mean():.2f}")
c2.metric("Số sinh viên đạt (≥ 5)", int((df["Tong_ket"] >= 5).sum()))
st.success(f"Cao nhất: {cao['Ho_ten']} – {cao['Tong_ket']}")
st.error(f"Thấp nhất: {thap['Ho_ten']} – {thap['Tong_ket']}")

st.subheader("Tra cứu sinh viên")
ten = st.selectbox("Chọn sinh viên:", df["Ho_ten"])
sv = df[df["Ho_ten"] == ten].iloc[0]
st.write(f"**Chuyên cần:** {sv['Chuyen_can']}")
st.write(f"**Giữa kỳ:** {sv['Giua_ky']}")
st.write(f"**Cuối kỳ:** {sv['Cuoi_ky']}")
st.write(f"**Điểm tổng kết:** {sv['Tong_ket']}")
st.write(f"**Xếp loại:** {sv['Xep_loai']}")

st.subheader("Biểu đồ điểm tổng kết")
fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(df["Ho_ten"], df["Tong_ket"], color="#5B9BF8")
ax.invert_yaxis()
ax.set_xlim(0, 10)
ax.set_xlabel("Điểm tổng kết")
ax.set_ylabel("Sinh viên")
ax.set_title("Điểm tổng kết của 10 sinh viên")
st.pyplot(fig)

# ---------- Chân trang ----------
st.markdown("---")
st.caption("Người thực hiện: Trần Việt Hoàng – MSSV: 025208009350")  
