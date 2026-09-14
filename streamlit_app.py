import pandas as pd
import streamlit as st

# إعداد الصفحة وتكوين العرض
st.set_page_config(
    page_title="دليلك في الخير", page_icon="🌟", layout="centered"
)

# تصميم وتنسيق CSS بروفيشنال وفخم (Dark Theme عصري)
st.markdown(
    """
    <style>
    .stApp { background-color: #0b0f19; color: #ffffff; direction: rtl; text-align: right; }
    
    /* البنر الرئيسي للموقع */
    .hero-banner {
        background: linear-gradient(135deg, #1f6feb 0%, #238636 100%);
        padding: 30px 20px;
        border-radius: 16px;
        text-align: center;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.5);
    }
    .hero-banner h1 { font-size: 32px !important; margin-bottom: 8px; color: #ffffff !important; }
    .hero-banner p { font-size: 16px !important; color: #e6edf3 !important; margin: 0; }

    /* كروت العرض الاحترافية */
    .service-card {
        background-color: #161b22;
        padding: 20px;
        border-radius: 14px;
        margin-bottom: 15px;
        border: 1px solid #30363d;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    
    h2, h3, h4 { color: #58a6ff !important; font-weight: bold !important; }
    p, label, span, .stMarkdown { color: #f0f6fc !important; font-size: 16px !important; }
    
    .stTextInput input, .stSelectbox select, .stTextArea textarea {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# واجهة البنر
st.markdown(
    """
    <div class="hero-banner">
        <h1>🌟 دليلك في الخير 🌟</h1>
        <p>المنصة الأسرع والأسهل للبحث عن الخدمات والأنشطة في منطقتك</p>
    </div>
""",
    unsafe_allow_html=True,
)

# رابط الشيت المباشر الخاص بك
REGIONS_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRo_K44P9J0mEaWBCH_d9_7Mhn3QGAxOKihLiWBVOyPSo8eR20mjgyt-jaclJ045i1jdDVwGwUruvCF/pub?gid=0&single=true&output=csv"


@st.cache_data(ttl=5)
def load_data(url):
  try:
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df
  except:
    return pd.DataFrame()


df_regions = load_data(REGIONS_SHEET_URL)

# القائمة الرئيسية للموقع
app_mode = st.selectbox(
    "القائمة الرئيسية:",
    [
        "🔍 تصفح الدليل والخدمات",
        "➕ اطلب إضافة خدمة أو نشاط جديد",
        "🔐 لوحة تحكم الأدمين",
    ],
)

if app_mode == "🔍 تصفح الدليل والخدمات":
  st.markdown("---")
  st.markdown("<h3>🔍 تصفح الخدمات والأنشطة</h3>", unsafe_allow_html=True)

  if not df_regions.empty:
    # جلب أول عمود كمرجع للمنطقة أو النشاط
    col_name = df_regions.columns[0]
    all_items = df_regions[col_name].dropna().astype(str).unique().tolist()

    selected_item = st.selectbox(
        "اختر أو ابحث:", ["اختر من القائمة..."] + all_items
    )

    if selected_item != "اختر من القائمة...":
      st.markdown(f"---")
      st.markdown(f"<h2>📍 تفاصيل العنصر: {selected_item}</h2>", unsafe_allow_html=True)

      filtered_data = df_regions[
          df_regions[col_name].astype(str) == selected_item
      ]

      for idx, row in filtered_data.iterrows():
        card_html = "<div class='service-card'>"
        for col in df_regions.columns:
          val = row[col]
          if pd.notna(val):
            card_html += f"<p><b>{col}:</b> {val}</p>"
        card_html += "</div>"
        st.markdown(card_html, unsafe_allow_html=True)
    else:
      st.info("💡 اختر عنصراً من القائمة أعلاه لعرض التفاصيل الكاملة.")
  else:
    st.warning(
        "⚠️ جدول البيانات فارغ حالياً أو بانتظار إضافات جديدة من الأنشطة."
    )

elif app_mode == "➕ اطلب إضافة خدمة أو نشاط جديد":
  st.markdown("---")
  st.markdown(
      "<h3>📝 نموذج تسجيل خدمة أو نشاط جديد</h3>", unsafe_allow_html=True
  )
  st.markdown(
      "<p style='color: #8b949e;'>أضف بيانات نشاطك بكل سهولة لتظهر في الدليل.</p>",
      unsafe_allow_html=True,
  )

  with st.form("add_service_form"):
    owner_name = st.text_input(
        "اسم صاحب النشاط / المسؤول:", placeholder="مثال: أحمد محمد"
    )
    service_name = st.text_input(
        "اسم الخدمة أو النشاط:", placeholder="مثال: صيدلية الشفاء / مطعم البرنس"
    )
    region_name = st.text_input(
        "المنطقة أو الحي:", placeholder="مثال: الخانكة - الشارع العمومي"
    )
    phone_number = st.text_input(
        "رقم الواتساب أو التواصل:", placeholder="مثال: 01127674550"
    )

    submit_btn = st.form_submit_button("إرسال الخدمة للدليل 🚀")

    if submit_btn:
      if (
          owner_name
          and service_name
          and region_name
          and phone_number
      ):
        st.success(
            "🎉 تم تسجيل طلبك بنجاح! سيتم مراجعته وإضافته في أسرع وقت."
        )
      else:
        st.error("⚠️ يرجى ملء كافة الحقول المطلوبة بشكل صحيح.")

else:
  st.markdown("---")
  st.markdown("<h3>🔐 لوحة تحكم الإدارة (الأدمين)</h3>", unsafe_allow_html=True)
  admin_pass = st.text_input(
      "كلمة المرور:", type="password", placeholder="اكتب كلمة المرور..."
  )

  if admin_pass == "Gemy@2026":
    st.success("✅ أهلاً بك يا كيمو، تم تسجيل الدخول بنجاح.")
    st.markdown("---")
    st.markdown("<h4>📋 البيانات الحالية في الشيت:</h4>", unsafe_allow_html=True)
    if not df_regions.empty:
      st.dataframe(df_regions, use_container_width=True)
    else:
      st.info("الشيت فارغ تماماً حالياً.")
  elif admin_pass:
    st.error("❌ كلمة المرور غير صحيحة.")
  else:
    st.info("💡 برجاء إدخال كلمة المرور (Gemy@2026) لفتح اللوحة.")
