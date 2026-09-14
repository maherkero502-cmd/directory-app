import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="دليل خدمات منطقتك", page_icon="📍", layout="centered"
)

# Professional CSS for Dark Theme, Clear Large Fonts, and 4x6 Thumbnails
st.markdown(
    """
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; direction: rtl; text-align: right; }
    .card { background-color: #161b22; padding: 20px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #30363d; box-shadow: 0 4px 6px rgba(0,0,0,0.4); }
    .ad-banner { background: linear-gradient(135deg, #1f6feb, #238636); padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px; color: white; font-weight: bold; font-size: 16px; }
    
    /* Clear and Large Text Formatting */
    h1, h2, h3 { color: #58a6ff !important; font-weight: bold !important; }
    p, label, span, .stMarkdown { color: #f0f6fc !important; font-size: 16px !important; }
    
    /* 4x6 Thumbnail Image Styling */
    .thumb-img { width: 120px; height: 180px; object-fit: cover; border-radius: 8px; border: 2px solid #30363d; margin-bottom: 10px; }
    
    .stSelectbox label, .stTextInput label, .stTextArea label, .stFileUploader label { color: #7ee787 !important; font-weight: bold !important; font-size: 17px !important; }
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
    "<p style='text-align: center; color: #8b949e; font-size: 18px;'>خدمات"
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

# Initialize Session State
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

if "pending_services" not in st.session_state:
  st.session_state["pending_services"] = []

if "main_ads_requests" not in st.session_state:
  st.session_state["main_ads_requests"] = []

# Main Navigation Menu
menu = st.selectbox(
    "القائمة الرئيسية:",
    [
        "🔍 تصفح الدليل والخدمات",
        "➕ إضافة خدمة أو نشاط جديد",
        "⭐ طلب إعلان على الصفحة الرئيسية",
        "⚙️ لوحة تحكم الإدارة (مراجعة وتعديل ونشر)",
    ],
)

if menu == "🔍 تصفح الدليل والخدمات":
  st.markdown("---")
  st.markdown("<h2>🔍 تصفح الخدمات المعتمدة</h2>", unsafe_allow_html=True)

  if st.session_state["services_list"]:
    existing_regions = list(
        set([s["region"] for s in st.session_state["services_list"]])
    )
    selected_region = st.selectbox("اختر المنطقة للتصفح:", existing_regions)

    existing_categories = list(
        set(
            [
                s["category"]
                for s in st.session_state["services_list"]
                if s["region"] == selected_region
            ]
        )
    )
    selected_category = st.selectbox(
        "اختر القسم أو الخدمة:", existing_categories
    )

    st.markdown(
        f"<h3>نتائج البحث في {selected_region} - {selected_category}</h3>",
        unsafe_allow_html=True,
    )

    matched_services = [
        s
        for s in st.session_state["services_list"]
        if s["region"] == selected_region and s["category"] == selected_category
    ]

    for s in matched_services:
      img_html = ""
      if s["image"] is not None:
        import base64

        if isinstance(s["image"], bytes):
          encoded_img = base64.b64encode(s["image"]).decode()
          img_html = f"<img src='data:image/jpeg;base64,{encoded_img}' class='thumb-img'>"
        else:
          img_html = f"<img src='{s['image']}' class='thumb-img'>"

      st.markdown(
          f"""
            <div class="card" style="display: flex; gap: 20px; align-items: center;">
                <div>{img_html}</div>
                <div style="flex-grow: 1;">
                    <h3 style="margin-top: 0; color: #58a6ff;">{s['name']}</h3>
                    <p style="color: #ffffff;"><b>التفاصيل:</b> {s['job']}</p>
                    <p style="color: #7ee787; font-size: 15px;"><b>التقييم:</b> {s['badge']}</p>
                    <hr style="border-color: #30363d;">
                    <p style="font-size: 13px; color: #8b949e;">لعرض اعلانك هنا تواصل مع الاداره: 01127674550</p>
                    <a href="https://wa.me/{s['phone']}" target="_blank" style="background-color: #238636; color: white; padding: 8px 16px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">تواصل عبر واتساب 💬</a>
                </div>
            </div>
            """,
          unsafe_allow_html=True,
      )
  else:
    st.info("لا توجد خدمات معتمدة حالياً في الدليل.")

elif menu == "➕ إضافة خدمة أو نشاط جديد":
  st.markdown("---")
  st.markdown("<h2>➕ أضف خدمتك أو نشاطك للدليل</h2>", unsafe_allow_html=True)
  st.markdown(
      "<p>املأ بيانات خدمتك، وسيتم إرسالها للإدارة للمراجعة والتأكيد قبل"
      " النشر.</p>",
      unsafe_allow_html=True,
  )

  with st.form("add_service_form"):
    p_name = st.text_input("اسم صاحب النشاط أو الخدمة:")
    p_region = st.text_input(
        "اكتب اسم منطقتك (مثال: الخانكة، ولو كتبت خطأ سيتم تصليحها):"
    )
    p_cat = st.text_input(
        "اكتب اسم الخدمة أو الوظيفة (مثال: سباك، صيدلية...):"
    )
    p_job = st.text_area("وصف الخدمة أو الإعلان بالتفصيل:")
    p_image_file = st.file_uploader(
        "ارفع صورة النشاط (صورة مصغرة 4×6):", type=["jpg", "png", "jpeg"]
    )
    p_phone = st.text_input("رقم الواتساب للتواصل (مثال: 201124214831):")
    p_badge = st.text_input(
        "الشارة أو التقييم المطلوب:", value="موصى به ⭐"
    )

    submit_button = st.form_submit_button(
        label="إرسال الخدمة للإدارة للمراجعة والنشر 🚀"
    )

    if submit_button:
      if p_name and p_phone and p_job and p_region and p_cat:
        img_bytes = p_image_file.read() if p_image_file else None
        st.session_state["pending_services"].append({
            "region": p_region.strip(),
            "category": p_cat.strip(),
            "name": p_name,
            "job": p_job,
            "image": img_bytes,
            "phone": p_phone,
            "badge": p_badge,
        })
        st.success(
            "تم إرسال طلبك بنجاح! سيتم مراجعته وتأكيده ونشره بواسطة الإدارة"
            " قريباً."
        )
      else:
        st.warning("من فضلك أكمل جميع الحقول الأساسية المطلوبة.")

elif menu == "⭐ طلب إعلان على الصفحة الرئيسية":
  st.markdown("---")
  st.markdown(
      "<h2>⭐ طلب إعلان مميز على الصفحة الرئيسية</h2>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<p>إذا كنت تريد تركيز إعلانك في الواجهة الرئيسية، اترك اسمك ورقم"
      " موبايلك فقط وسنتواصل معك!</p>",
      unsafe_allow_html=True,
  )

  with st.form("main_ad_form"):
    ad_name = st.text_input("الاسم الكريم:")
    ad_phone = st.text_input("رقم الموبايل للتواصل:")
    ad_submit = st.form_submit_button(
        label="إرسال طلب الإعلان الرئيسي للضرورة 🚀"
    )

    if ad_submit:
      if ad_name and ad_phone:
        st.session_state["main_ads_requests"].append(
            {"name": ad_name, "phone": ad_phone}
        )
        st.success(
            "تم استلام طلبك بنجاح، وسيقوم فريق الإدارة بالتواصل معك في أقرب وقت!"
        )
      else:
        st.warning("يرجى إدخال الاسم ورقم الموبايل بشكل صحيح.")

else:
  st.markdown("---")
  st.markdown(
      "<h2>⚙️ لوحة تحكم الإدارة (مراجعة، تعديل وتأكيد النشر)</h2>",
      unsafe_allow_html=True,
  )

  ADMIN_PASSWORD = "Kero@2026"
  admin_pass = st.text_input(
      "أدخل كلمة مرور الإدارة السرية:", type="password"
  )

  if admin_pass == ADMIN_PASSWORD:
    st.success("مرحباً بك يا كيمو! هذه هي الطلبات الجديدة التي تنتظر مراجعتك:")

    if st.session_state["pending_services"]:
      for idx, s in enumerate(st.session_state["pending_services"]):
        st.markdown(f"---")
        st.write(
            f"**طلب معلق #{idx + 1}** | **الاسم:** {s['name']} |"
            f" **المنطقة:** {s['region']} | **القسم:** {s['category']}"
        )
        st.write(f"**التفاصيل:** {s['job']} | **الهاتف:** {s['phone']}")

        # Action buttons for admin
        col1, col2 = st.columns(2)
        with col1:
          if st.button(
              f"تأكيد ونشر مباشر في الدليل ✅", key=f"approve_{idx}"
          ):
            st.session_state["services_list"].append(s)
            st.session_state["pending_services"].pop(idx)
            st.success("تم تأكيد النشر وأصبحت الخدمة ظاهرة في الدليل!")
            st.rerun()
        with col2:
          if st.button(f"رفض وإلغاء ❌", key=f"reject_{idx}"):
            st.session_state["pending_services"].pop(idx)
            st.success("تم رفض الطلب.")
            st.rerun()

        # Option to edit before publishing (fixes misspellings like "خانكي" to "الخانكة")
        with st.expander(f"✏️ تعديل الخطأ الإملائي قبل النشر للطلب #{idx + 1}"):
          with st.form(key=f"edit_pending_form_{idx}"):
            new_region = st.text_input(
                "تعديل المنطقة (مثل تصحيح خانكي إلى الخانكة):",
                value=s["region"],
            )
            new_cat = st.text_input("تعديل القسم:", value=s["category"])
            new_name = st.text_input("تعديل الاسم:", value=s["name"])
            new_job = st.text_area("تعديل الوصف:", value=s["job"])
            save_and_publish = st.form_submit_button(
                "حفظ التعديلات وتأكيد النشر فوراً 💾🚀"
            )

            if save_and_publish:
              s["region"] = new_region.strip()
              s["category"] = new_cat.strip()
              s["name"] = new_name.strip()
              s["job"] = new_job.strip()
              st.session_state["services_list"].append(s)
              st.session_state["pending_services"].pop(idx)
              st.success(
                  "تم تعديل الخطأ الإملائي وتأكيد نشر الخدمة في الدليل بنجاح!"
              )
              st.rerun()
    else:
      st.info("لا توجد طلبات معلقة حالياً تنتظر المراجعة.")

    st.markdown("---")
    st.markdown(
        "<h3>⭐ طلبات الإعلانات الرئيسية (اسم ورقم فقط)</h3>",
        unsafe_allow_html=True,
    )
    if st.session_state["main_ads_requests"]:
      for m_idx, req in enumerate(st.session_state["main_ads_requests"]):
        st.write(
            f"**{m_idx + 1}. الاسم:** {req['name']} | **الهاتف:**"
            f" {req['phone']}"
        )
        if st.button(f"حذف الطلب 🗑️", key=f"del_main_{m_idx}"):
          st.session_state["main_ads_requests"].pop(m_idx)
          st.rerun()
    else:
      st.info("لا توجد طلبات إعلانات رئيسية حالياً.")

  elif admin_pass != "":
    st.error("كلمة المرور غير صحيحة!")
  else:
    st.info("أدخل كلمة المرور الخاصة بك لعرض الطلبات المعلقة ومراجعتها.")
