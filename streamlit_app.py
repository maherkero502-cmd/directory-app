import pandas as pd
import requests
import streamlit as st

# إعداد الصفحة
st.set_page_config(
    page_title="دليلك في الخير", page_icon="🌟", layout="centered"
)

# تنسيق التصميم العصري (Dark Theme)
st.markdown(
    """
    <style>
    .stApp { background-color: #0b0f19; color: #ffffff; direction: rtl; text-align: right; }
    
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

# البنر الرئيسي
st.markdown(
    """
    <div class="hero-banner">
        <h1>🌟 دليلك في الخير 🌟</h1>
        <p>المنصة الأسرع والأسهل للبحث عن الخدمات والأنشطة في منطقتك</p>
    </div>
""",
    unsafe_allow_html=True,
)

# روابط الشيت والـ Apps Script
FULL_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRo_K44P9J0mEaWBCH_d9_7Mhn3QGAxOKihLiWBVOyPSo8eR20mjgyt-jaclJ045i1jdDVwGwUruvCF/pub?output=csv"
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyUtpSF0ia-TFPjNSea6bTnI6s-bIUiv0iQ1h84_8m8aSYWp3WX11wmTRIGj-5nYWnYSQ/exec"


@st.cache_data(ttl=5)
def load_data(url):
  try:
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df
  except:
    return pd.DataFrame()


df_main = load_data(FULL_SHEET_URL)

# القائمة الرئيسية
app_mode = st.selectbox(
    "القائمة الرئيسية:",
    [
        "🔍 تصفح الدليل والخدمات",
        "➕ اطلب إضافة خدمة أو نشاط جديد",
        "🔐 لوحة تحكم الإدارة",
    ],
)

if app_mode == "🔍 تصفح الدليل والخدمات":
  st.markdown("---")
  st.markdown("<h3>🔍 تصفح الخدمات والأنشطة</h3>", unsafe_allow_html=True)

  if not df_main.empty:
    col_name = df_main.columns[0]
    all_items = df_main[col_name].dropna().astype(str).unique().tolist()

    selected_item = st.selectbox(
        "اختر أو ابحث:", ["اختر من القائمة..."] + all_items
    )

    if selected_item != "اختر من القائمة...":
      st.markdown(f"---")
      st.markdown(f"<h2>📍 تفاصيل العنصر: {selected_item}</h2>", unsafe_allow_html=True)

      filtered_data = df_main[df_main[col_name].astype(str) == selected_item]

      for idx, row in filtered_data.iterrows():
        card_html = "<div class='service-card'>"
        for col in df_main.columns:
          val = row[col]
          if pd.notna(val):
            card_html += f"<p><b>{col}:</b> {val}</p>"
        card_html += "</div>"
        st.markdown(card_html, unsafe_allow_html=True)
    else:
      st.info("💡 اختر عنصراً من القائمة أعلاه لعرض التفاصيل الكاملة.")
  else:
    st.warning("⚠️ جدول البيانات فارغ حالياً.")

elif app_mode == "➕ اطلب إضافة خدمة أو نشاط جديد":
  st.markdown("---")
  st.markdown(
      "<h3>📝 نموذج تسجيل خدمة أو نشاط جديد</h3>", unsafe_allow_html=True
  )
  st.markdown(
      "<p style='color: #8b949e;'>أضف بيانات نشاطك لتصل للإدارة وتظهر في الدليل"
      " بعد المراجعة.</p>",
      unsafe_allow_html=True,
  )

  with st.form("add_service_form"):
    owner_name = st.text_input(
        "اسم صاحب النشاط / المسؤول:", placeholder="مثال: أحمد محمد"
    )
    service_name = st.text_input(
        "اسم الخدمة أو النشاط:", placeholder="مثال: صيدلية الشفاء"
    )
    region_name = st.text_input(
        "المنطقة أو الحي:", placeholder="مثال: الخانكة"
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
        payload = {
            "owner_name": owner_name,
            "service_name": service_name,
            "region_name": region_name,
            "phone_number": phone_number,
        }
        try:
          response = requests.post(APPS_SCRIPT_URL, json=payload)
          if response.status_code == 200:
            st.success(
                "🎉 تم إرسال طلبك بنجاح! سيتم مراجعته وعرضه في الدليل قريباً."
            )
          else:
            st.warning("⚠️ تم الإرسال، تحقق من لوحة التحكم.")
        except Exception as e:
          st.error(f"❌ حدث خطأ: {e}")
      else:
        st.error("⚠️ يرجى ملء كافة الحقول المطلوبة.")

else:
  st.markdown("---")
  st.markdown("<h3>🔐 لوحة تحكم الإدارة (الأدمين)</h3>", unsafe_allow_html=True)
  admin_pass = st.text_input(
      "كلمة المرور:", type="password", placeholder="اكتب كلمة المرور..."
  )

  if admin_pass == "Gemy@2026":
    st.success("✅ أهلاً بك يا كيمو، تم تسجيل الدخول بنجاح.")
    st.markdown("---")
    st.markdown("<h4>📥 مراجعة الطلبات الجديدة الواردة:</h4>", unsafe_allow_html=True)
    st.info(
        "💡 أي طلب جديد سيتم تسجيله عبر النموذج سيظهر هنا في الشيت، ويمكنك"
        " مراجعته ونقله للجدول الرئيسي مباشرة."
    )

    st.markdown("<h4>📋 محتوى الشيت الحالي:</h4>", unsafe_allow_html=True)
    if not df_main.empty:
      st.dataframe(df_main, use_container_width=True)
    else:
      st.info("الشيت فارغ حالياً.")
  elif admin_pass:
    st.error("❌ كلمة المرور غير صحيحة.")
  else:
    st.info("💡 برجاء إدخال كلمة المرور الصحيحة (Gemy@2026).")
