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
    .card { background-color: #161b22; padding: 20px; border-radius: 12px; margin-bottom: 15px; border: 1px solid #30363d; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .stSelectbox label, .stTextInput label, .stTextArea label { color: #58a6ff; font-weight: bold; }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("📍 دليل خدمات الخانكة والسلام والمرج")
st.write(
    "منصتك المحلية الشاملة لاختيار الخدمات ومقدمي الإعلانات مباشرة عبر واتساب."
)

# Initialize Session State for dynamic services list
if "services_list" not in st.session_state:
  st.session_state["services_list"] = [{
      "region": "الخانكة",
      "category": "سباك",
      "name": "الأسطفى محمد",
      "job": "صيانة سباكة منزلية وتأسيس",
      "phone": "201124214831",
      "badge": "مميز ⭐",
  }]

# Sidebar or Tabs for Navigation
menu = st.selectbox(
    "القائمة الرئيسية:", ["🔍 تصفح الدليل والخدمات", "➕ أضف إعلانك / خدمتك مجاناً"]
)

if menu == "🔍 تصفح الدليل والخدمات":
  st.markdown("---")
  regions = ["الخانكة", "السلام", "المرج", "عين شمس"]
  selected_region = st.selectbox("اختر المنطقة:", regions)

  # Filter categories based on region
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

  # Filter services
  matched_services = [
      s
      for s in st.session_state["services_list"]
      if s["region"] == selected_region and s["category"] == selected_category
  ]

  if matched_services:
    for s in matched_services:
      st.markdown(
          f"""
            <div class="card">
                <h3>{s['name']}</h3>
                <p><b>الخدمة / الإعلان:</b> {s['job']}</p>
                <p><b>التصنيف:</b> {s['badge']}</p>
                <a href="https://wa.me/{s['phone']}" target="_blank" style="background-color: #238636; color: white; padding: 10px 20px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block; margin-top: 10px;">تواصل عبر واتساب 💬</a>
            </div>
            """,
          unsafe_allow_html=True,
      )
  else:
    st.info(
        "لا توجد إعلانات أو خدمات مضافة في هذا القسم حالياً. يمكنك إضافتها"
        " بنفسك من قائمة (أضف إعلانك)!"
    )

else:
  st.markdown("### ➕ إضافة إعلان أو خدمة جديدة للدليل")
  with st.form("add_service_form"):
    p_name = st.text_input("اسم صاحب الخدمة أو النشاط:")
    p_region = st.selectbox(
        "المنطقة:", ["الخانكة", "السلام", "المرج", "عين شمس"]
    )
    p_cat = st.selectbox(
        "القسم:",
        ["سباك", "سواق توك توك", "صيدليات", "عربية ملاكي", "كافيه", "مطعم", "أخرى"],
    )
    p_job = st.text_area("تفاصيل الخدمة أو الإعلان:")
    p_phone = st.text_input(
        "رقم الواتساب (مثال: 201124214831 بدون علامة +):"
    )
    p_badge = st.text_input("شارة أو تقييم (اختياري مثل: معتمد ⭐):", value="جديد")

    submit_button = st.form_submit_button(
        label="نشر الإعلان فوراً في الدليل 🚀"
    )

    if submit_button:
      if p_name and p_phone and p_job:
        st.session_state["services_list"].append({
            "region": p_region,
            "category": p_cat,
            "name": p_name,
            "job": p_job,
            "phone": p_phone,
            "badge": p_badge,
        })
        st.success(
            "تم إضافة إعلانك بنجاح! انتقل إلى (تصفح الدليل والخدمات) لرؤيته"
            " فوراً."
        )
      else:
        st.warning("من فضلك املأ الحقول الأساسية (الاسم، التفاصيل، ورقم الهاتف).")
