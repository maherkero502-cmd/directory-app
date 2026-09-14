import streamlit as st

st.set_page_config(
    page_title="دليل خدمات الخانكة والسلام والمرج",
    page_icon="📍",
    layout="centered",
)

# Dark Theme & RTL CSS Support
st.markdown(
    """
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; direction: rtl; text-align: right; }
    .card { background-color: #161b22; padding: 20px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #30363d; box-shadow: 0 4px 6px rgba(0,0,0,0.4); }
    .ad-banner { background: linear-gradient(135deg, #1f6feb, #238636); padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px; color: white; font-weight: bold; }
    .stSelectbox label, .stTextInput label, .stTextArea label { color: #58a6ff; font-weight: bold; }
    </style>
""",
    unsafe_allow_html=True,
)

# App Header & Logo Display
st.markdown(
    "<h1 style='text-align: center;'>📍 دليل خدمات الخانكة والسلام والمرج</h1>",
    unsafe_allow_html=True,
)

# Displaying the user uploaded logo nicely
st.image(
    "https://raw.githubusercontent.com/maherkero502-cmd/directory-app/main/logo.png",
    use_container_width=True,
)
# (Fallback text if image is uploading)
st.markdown(
    "<p style='text-align: center; color: #8b949e; font-size: 16px;'>خدمات"
    " منطقتك في مكان واحد 🌟</p>",
    unsafe_allow_html=True,
)

# Professional Ad Space Banner
st.markdown(
    """
    <div class="ad-banner">
        📢 لعرض إعلانك أو نشاطك هنا بشكل مميز، تواصل مع الإدارة عبر الواتساب: 01127674550
    </div>
""",
    unsafe_allow_html=True,
)

# Initialize Session State (Cleaned up, no old dummy plumber data)
if "services_list" not in st.session_state:
  st.session_state["services_list"] = []

# Navigation Menu
menu = st.selectbox(
    "القائمة الرئيسية:", ["🔍 تصفح الدليل والخدمات", "➕ أضف إعلانك أو خدمتك"]
)

if menu == "🔍 تصفح الدليل والخدمات":
  st.markdown("---")
  regions = ["الخانكة", "السلام", "المرج", "عين شمس"]
  selected_region = st.selectbox("اختر المنطقة:", regions)

  categories = [
      "سباك",
      "سواق توك توك",
      "صيدليات",
      "عربية ملاكي",
      "كافيه",
      "مطعم",
      "أخرى",
  ]
  selected_category = st.selectbox("اختر القسم:", categories)

  st.markdown(f"### نتائج البحث في {selected_region} - {selected_category}")

  matched_services = [
      s
      for s in st.session_state["services_list"]
      if s["region"] == selected_region and s["category"] == selected_category
  ]

  if matched_services:
    for s in matched_services:
      img_tag = (
          f"<img src='{s['image']}' style='width:100%; height:180px;"
          " object-fit: cover; border-radius: 8px; margin-bottom: 10px;'>"
          if s["image"]
          else ""
      )
      st.markdown(
          f"""
            <div class="card">
                {img_tag}
                <h3 style="margin-top: 5px;">{s['name']}</h3>
                <p><b>التفاصيل:</b> {s['job']}</p>
                <p style="color: #f0883e; font-size: 14px;"><b>التقييم/الشارة:</b> {s['badge']}</p>
                <hr style="border-color: #30363d;">
                <p style="font-size: 13px; color: #8b949e; margin-bottom: 10px;">لعرض اعلانك هنا تواصل مع الاداره: 01127674550</p>
                <a href="https://wa.me/{s['phone']}" target="_blank" style="background-color: #238636; color: white; padding: 10px 20px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">تواصل عبر واتساب 💬</a>
            </div>
            """,
          unsafe_allow_html=True,
      )
  else:
    st.info(
        "لا توجد إعلانات مضافة في هذا القسم حتى الآن. كن أول المنضمين وأضف"
        " إعلانك الآن!"
    )

else:
  st.markdown("### ➕ إضافة إعلان أو نشاط جديد للدليل")
  with st.form("add_service_form"):
    p_name = st.text_input("اسم صاحب النشاط أو الإعلان:")
    p_region = st.selectbox(
        "اختر المنطقة:", ["الخانكة", "السلام", "المرج", "عين شمس"]
    )
    p_cat = st.selectbox(
        "اختر القسم:",
        ["سباك", "سواق توك توك", "صيدليات", "عربية ملاكي", "كافيه", "مطعم", "أخرى"],
    )
    p_job = st.text_area("وصف الخدمة أو الإعلان بالتفصيل:")
    p_image = st.text_input(
        "رابط صورة الإعلان (اختياري - رابط مباشر للصورة):"
    )
    p_phone = st.text_input(
        "رقم الواتساب للتواصل (مثال: 201124214831 بدون علامة +):"
    )
    p_badge = st.text_input(
        "الشارة أو التقييم (مثال: مميز ⭐ / معتمد):", value="معتمد ⭐"
    )

    submit_button = st.form_submit_button(
        label="نشر الإعلان في الدليل مباشرة 🚀"
    )

    if submit_button:
      if p_name and p_phone and p_job:
        st.session_state["services_list"].append({
            "region": p_region,
            "category": p_cat,
            "name": p_name,
            "job": p_job,
            "image": p_image,
            "phone": p_phone,
            "badge": p_badge,
        })
        st.success(
            "تم نشر الإعلان بنجاح! انتقل إلى (تصفح الدليل والخدمات) لمشاهدته"
            " بشكله الجديد."
        )
      else:
        st.warning(
            "من فضلك أكمل الحقول الأساسية (الاسم، التفاصيل، ورقم الواتساب)."
        )
