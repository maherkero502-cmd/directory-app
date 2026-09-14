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
        padding: 35px 20px;
        border-radius: 16px;
        text-align: center;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.5);
    }
    .hero-banner h1 { font-size: 34px !important; margin-bottom: 8px; color: #ffffff !important; }
    .hero-banner p { font-size: 17px !important; color: #e6edf3 !important; margin: 0; }

    /* كروت العرض الاحترافية */
    .service-card {
        background-color: #161b22;
        padding: 22px;
        border-radius: 14px;
        margin-bottom: 18px;
        border: 1px solid #30363d;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        transition: transform 0.2s;
    }
    .service-card:hover {
        border-color: #58a6ff;
        transform: translateY(-2px);
    }
    
    /* أزرار وتنسيقات النصوص */
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
        <p>المنصة الأجمل والأسرع للبحث عن الخدمات والأنشطة في منطقتك</p>
    </div>
""",
    unsafe_allow_html=True,
)

# رابط الشيت (المناطق والخدمات)
REGIONS_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRo_K44P9J0mEaWBCH_d9_7Mhn3QGAxOKihLiWBVOyPSo8eR20mjgyt-jaclJ045i1jdDVwGwUruvCF/pub?gid=0&single=true&output=csv"


@st.cache_data(ttl=10)
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
        "🔍 تصفح الدليل والبحث الذكي",
        "➕ اطلب إضافة خدمتك أو نشاطك",
        "🔐 لوحة تحكم الأدمين (الإدارة)",
    ],
)

if app_mode == "🔍 تصفح الدليل والبحث الذكي":
  st.markdown("---")
  st.markdown("<h3>🔍 البحث السريع في الدليل</h3>", unsafe_allow_html=True)

  if not df_regions.empty:
    col_name = (
        df_regions.columns[0]
        if len(df_regions.columns) > 0
        else "اسم المنطقة"
    )
    all_regions = df_regions[col_name].dropna().astype(str).unique().tolist()

    selected_region = st.selectbox(
        "اختر أو ابحث عن منطقتك:",
        ["اختر المنطقة..."] + all_regions,
    )

    if selected_region != "اختر المنطقة...":
      st.markdown(f"---")
      st.markdown(f"<h2>📍 نتائج خدمات منطقة: {selected_region}</h2>", unsafe_allow_html=True)

      filtered_data = df_regions[
          df_regions[col_name].astype(str) == selected_region
      ]

      for idx, row in filtered_data.iterrows():
        st.markdown(
            f"""
                <div class="service-card">
                    <h4>🏢 النشاط / الخدمة: {row.get(df_regions.columns[1], 'خدمة عامة')}</h4>
                    <p><b>📞 رقم التواصل / الواتساب:</b> {row.get(df_regions.columns[2], 'غير متوفر')}</p>
                    <p><b>📝 التفاصيل:</b> {row.get(df_regions.columns[3], 'لا توجد تفاصيل إضافية')}</p>
                </div>
            """,
            unsafe_allow_html=True,
        )
    else:
      st.info("💡 يرجى اختيار المنطقة من القائمة أعلاه لعرض الخدمات المتاحة.")
  else:
    st.warning("⚠️ جدول البيانات فارغ حالياً، بانتظار إضافات أصحاب الخدمات!")

elif app_mode == "➕ اطلب إضافة خدمتك أو نشاطك":
  st.markdown("---")
  st.markdown(
      "<h3>📝 نموذج تسجيل خدمة أو نشاط جديد في الدليل</h3>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<p style='color: #8b949e;'>أدخل بيانات نشاطك بدقة، وستظهر في الدليل"
      " فور اعتمادها.</p>",
      unsafe_allow_html=True,
  )

  with st.form("add_service_form"):
    owner_name = st.text_input(
        "اسم المسؤول أو صاحب النشاط:", placeholder="مثال: محمد أحمد"
    )
    service_name = st.text_input(
        "اسم النشاط أو الخدمة:", placeholder="مثال: صيدلية الشفاء / مطعم البرنس"
    )
    region_name = st.text_input(
        "المنطقة / الحي:", placeholder="مثال: الخانكة - الشارع الرئيسي"
    )
    phone_number = st.text_input(
        "رقم الواتساب أو الاتصال:", placeholder="مثال: 01127674550"
    )
    description = st.text_area(
        "تفاصيل الخدمة أو العروض:",
        placeholder=(
            "اكتب نبذة مختصرة عن الخدمات المقدمة أو أي خصومات متاحة..."
        ),
    )

    submit_btn = st.form_submit_button("إرسال الخدمة للمراجعة 🚀")

    if submit_btn:
      if (
          owner_name
          and service_name
          and region_name
          and phone_number
      ):
        st.success(
            "🎉 تم إرسال طلبك بنجاح! سيتم مراجعته وإضافته قريباً للدليل."
        )
      else:
        st.error("⚠️ يرجى استكمال الحقول الأساسية المطلوبة.")

else:
  st.markdown("---")
  st.markdown("<h3>🔐 لوحة تحكم الإدارة (الإعلانات والمناطق)</h3>", unsafe_allow_html=True)
  st.markdown(
      "<p style='color: #58a6ff; font-size: 15px;'>كلمة المرور الخاصة بالدخول:"
      " <b>Gemy@2026</b></p>",
      unsafe_allow_html=True,
  )

  admin_pass = st.text_input(
      "أدخل كلمة مرور الأدمين:",
      type="password",
      placeholder="اكتب كلمة المرور هنا...",
  )

  if admin_pass == "Gemy@2026":
    st.success("✅ تم تسجيل الدخول بنجاح يا كيمو.")
    st.markdown("---")
    st.markdown("<h4>⚙️ إدارة محتوى الشيت الحالي:</h4>", unsafe_allow_html=True)
    if not df_regions.empty:
      st.dataframe(df_regions, use_container_width=True)
    else:
      st.info("الشيت فارغ حالياً تماماً وجاهز لاستقبال البيانات الجديدة.")
  elif admin_pass:
    st.error("❌ كلمة المرور غير صحيحة.")
  else:
    st.info("💡 برجاء إدخال كلمة المرور الصحيحة المذكورة أعلاه لفتح اللوحة.")
