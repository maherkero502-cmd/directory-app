import streamlit as st

st.set_page_config(
    page_title="دليل الخدمات المحلي", page_icon="📍", layout="centered"
)

# Dark Theme Custom CSS
st.markdown(
    """
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .card { background-color: #161b22; padding: 20px; border-radius: 10px; margin-bottom: 15px; border: 1px solid #30363d; }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("📍 دليل خدمات الخانكة والسلام والمرج")
st.write(
    "اختر المنطقة لمعرض الأقسام، وتواصل مباشرة مع مقدم الخدمة عبر واتساب."
)

regions = ["الخانكة", "السلام", "المرج", "عين شمس"]
selected_region = st.selectbox("اختر المنطقة:", regions)

if selected_region == "الخانكة":
  st.markdown("### الأقسام المتاحة في الخانكة")
  category = st.selectbox("اختر القسم:", ["سباك", "سواق توك توك", "صيدليات"])

  if category == "سباك":
    st.markdown(
        """
        <div class="card">
            <h3>الأسطفى محمد</h3>
            <p><b>الخدمة:</b> صيانة سباكة منزلية وتأسيس</p>
            <p><b>التقييم:</b> مميز ⭐</p>
            <a href="https://wa.me/201124214831" target="_blank" style="background-color: #25D366; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">تواصل عبر واتساب</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
  else:
    st.info("لا توجد خدمات مضافة في هذا القسم حالياً.")
else:
  st.info(f"جاري إضافة الخدمات لمنطقة {selected_region} قريباً...")
