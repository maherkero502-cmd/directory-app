import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="دليل خدمات منطقتك", page_icon="📍", layout="centered"
)

# Dark Theme & RTL CSS Support
st.markdown(
    """
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; direction: rtl; text-align: right; }
    .card { background-color: #161b22; padding: 20px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #30363d; box-shadow: 0 4px 6px rgba(0,0,0,0.4); }
    .ad-banner { background: linear-gradient(135deg, #1f6feb, #238636); padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px; color: white; font-weight: bold; }
    .stSelectbox label, .stTextInput label, .stTextArea label, .stFileUploader label { color: #58a6ff; font-weight: bold; }
    </style>
""",
    unsafe_allow_html=True,
)

# App Header & Logo Display
st.markdown(
    "<h1 style='text-align: center;'>📍 دليل خدمات منطقتك</h1>",
    unsafe_allow_html=True,
)

try:
  st.image("logo.jpg", use_container_width=True)
except:
  st.markdown(
      "<h3 style='text-align: center; color: #58a6ff;'>دليلك في الخير</h3>",
      unsafe_allow_html=True,
  )

st.markdown(
    "<p style='text-align: center; color: #8b949e; font-size: 16px;'>خدمات"
    " منطقتك وكل المدن في مكان واحد 🌟</p>",
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

# Initialize Session State with a default storage list
if "services_list" not in st.session_state:
  st.session_state["services_list"] = [
      {
          "region": "الخانكة",
          "category": "صيدليات",
          "name": "صيدلية الشفاء",
          "job": "خدمة أدوية ومستحضرات تجميل طوال اليوم",
          "image": None,
          "phone": "201124214831",
          "badge": "معتمد ⭐",
      }
  ]

# Navigation Menu (Including Admin Dashboard for you)
menu = st.selectbox(
    "القائمة الرئيسية:",
    [
        "🔍 تصفح الدليل والخدمات",
        "➕ أضف إعلانك أو منطقتك",
        "⚙️ لوحة تحكم الإدارة (خاصة بك)",
    ],
)

if menu == "🔍 تصفح الدليل والخدمات":
  st.markdown("---")

  existing_regions = list(
      set([s["region"] for s in st.session_state["services_list"]])
  )
  selected_region = st.selectbox(
      "اختر المنطقة للتصفح:", existing_regions if existing_regions else ["الخانكة"]
  )

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
      if s["image"] is not None:
        st.image(
            s["image"], use_container_width=True, caption=s["name"]
        )

      st.markdown(
          f"""
            <div class="card">
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
        "لا توجد إعلانات مضافة في هذا القسم والمنطقة حتى الآن. كن أول من يضيف"
        " إعلان ومنطقة جديدة!"
    )

elif menu == "➕ أضف إعلانك أو منطقتك":
  st.markdown("### ➕ إضافة إعلان أو منطقة جديدة للدليل")
  st.info(
      "املأ البيانات التالية، يمكنك كتابة اسم منطقتك الجديدة مباشرة، وسيتم نشرها"
      " فوراً!"
  )

  with st.form("add_service_form"):
    p_name = st.text_input("اسم صاحب النشاط أو الإعلان:")

    # Clean text input for region to avoid any bugs
    p_region = st.text_input(
        "اكتب اسم منطقتك أو مدينتك (مثال: الخانكة، شبرا، المرج، طوخ...):"
    )

    p_cat = st.selectbox(
        "اختر القسم:",
        ["سباك", "سواق توك توك", "صيدليات", "عربية ملاكي", "كافيه", "مطعم", "أخرى"],
    )
    p_job = st.text_area("وصف الخدمة أو الإعلان بالتفصيل:")

    p_image_file = st.file_uploader(
        "ارفع صورة النشاط أو صورتك الشخصية:", type=["jpg", "png", "jpeg"]
    )

    p_phone = st.text_input(
        "رقم الواتساب للتواصل (مثال: 201124214831 بدون علامة +):"
    )
    p_badge = st.text_input(
        "الشارة أو التقييم (مثال: مميز ⭐ / معتمد):", value="جديد 🌟"
    )

    submit_button = st.form_submit_button(
        label="نشر الإعلان والمنطقة في الدليل مباشرة 🚀"
    )

    if submit_button:
      if p_name and p_phone and p_job and p_region:
        st.session_state["services_list"].append({
            "region": p_region.strip(),
            "category": p_cat,
            "name": p_name,
            "job": p_job,
            "image": p_image_file,
            "phone": p_phone,
            "badge": p_badge,
        })
        st.success(
            "تم إضافة المنطقة والإعلان بنجاح! انتقل إلى (تصفح الدليل والخدمات)"
            " لرؤيتها."
        )
      else:
        st.warning(
            "من فضلك أكمل الحقول الأساسية (الاسم، اسم المنطقة، الوصف، ورقم"
            " الواتساب)."
        )

else:
  st.markdown("### ⚙️ لوحة تحكم الإدارة (التحكم في الإعلانات والمناطق)")
  admin_pass = st.text_input("Gemy@2026", type="password")

  # You can change '1234' to any password you like
  if admin_pass == "1234":
    st.success("مرحباً بك يا مدير الموقع! هذه هي جميع الإعلانات المضافة حالياً:")

    if st.session_state["services_list"]:
      for idx, s in enumerate(st.session_state["services_list"]):
        st.markdown(f"---")
        st.write(
            f"**رقم الإعلان:** {idx + 1} | **الاسم:** {s['name']} |"
            f" **المنطقة:** {s['region']} | **القسم:** {s['category']}"
        )
        st.write(f"**التفاصيل:** {s['job']} | **الهاتف:** {s['phone']}")

        if st.button(f"حذف هذا الإعلان ❌", key=f"del_{idx}"):
          st.session_state["services_list"].pop(idx)
          st.rerun()
    else:
      st.info("لا توجد إعلانات مضافة حتى الآن.")
  elif admin_pass != "":
    st.error("كلمة المرور غير صحيحة!")
  else:
    st.info("الرجاء إدخال كلمة المرور لعرض لوحة التحكم. (كلمة المرور التجريبية: 1234)")
