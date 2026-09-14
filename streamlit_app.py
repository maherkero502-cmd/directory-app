import pandas as pd
import streamlit as st

# إعداد الصفحة وتكوين العرض
st.set_page_config(
    page_title="دليلك في الخير", page_icon="📍", layout="centered"
)

# تصميم وتنسيق CSS بروفيشنال للشكل الجذاب والثيم الداكن الفخم
st.markdown(
    """
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; direction: rtl; text-align: right; }
    
    /* تصميم البنر الرئيسي في الواجهة */
    .hero-banner {
        background: linear-gradient(135deg, #1f6feb 0%, #238636 100%);
        padding: 30px 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.5);
    }
    .hero-banner h1 {
        font-size: 32px !important;
        margin-bottom: 10px;
        color: #ffffff !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    .hero-banner p {
        font-size: 18px !important;
        color: #e6edf3 !important;
        margin: 0;
    }

    /* تصميم الكروت للمناطق والخدمات */
    .region-card {
        background-color: #161b22;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
        border: 1px solid #30363d;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: transform 0.2s;
    }
    .region-card:hover {
        border-color: #58a6ff;
        transform: translateY(-2px);
    }

    h2, h3 { color: #58a6ff !important; font-weight: bold !important; }
    p, label, span, .stMarkdown { color: #f0f6fc !important; font-size: 16px !important; }
    
    /* تنسيق مربعات الإدخال والبحث */
    .stTextInput input {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
    }
    .stTextInput label { color: #7ee787 !important; font-weight: bold !important; font-size: 17px !important; }
    </style>
""",
    unsafe_allow_html=True,
)

# واجهة البنر الرئيسي في الأعلى
st.markdown(
    """
    <div class="hero-banner">
        <h1>🌟 دليلك في الخير 🌟</h1>
        <p>دليلك الشامل للخدمات والأنشطة في منطقتك.. الكل في خدمتكم</p>
    </div>
""",
    unsafe_allow_html=True,
)

# رابط الشيت المباشر (تبويب المناطق)
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRo_K44P9J0mEaWBCH_d9_7Mhn3QGAxOKihLiWBVOyPSo8eR20mjgyt-jaclJ045i1jdDVwGwUruvCF/pub?gid=0&single=true&output=csv"


# دالة قراءة البيانات مع التخزين المؤقت لسرعة التحميل
@st.cache_data(ttl=30)
def load_data(url):
  try:
    df = pd.read_csv(url)
    # تنظيف أسماء الأعمدة من المسافات الزائدة
    df.columns = df.columns.str.strip()
    return df
  except Exception as e:
    return pd.DataFrame()


# جلب البيانات
df_regions = load_data(SHEET_URL)

# شريط التنقل الجانبي أو القائمة الرئيسية
menu = st.selectbox(
    "اختر قسم التصفح:",
    ["📍 استعراض المناطق والبحث", "➕ إضافة منطقة جديدة (عبر الشيت)"],
)

if menu == "📍 استعراض المناطق والبحث":
  st.markdown("---")
  st.markdown("<h3>🔍 ابحث عن منطقتك المفضلة</h3>", unsafe_allow_html=True)

  if not df_regions.empty:
    # خانة البحث السريع
    search_query = st.text_input(
        "اكتب اسم المنطقة للبحث عنها:", placeholder="مثال: الخانكة، المرج..."
    )

    # تصفية البيانات بناءً على البحث
    if search_query:
      # البحث في أول عمود متاح أو عمود يحتوي على اسم المنطقة
      col_name = df_regions.columns[
          0
      ]  # افتراض أن العمود الأول هو اسم المنطقة
      filtered_df = df_regions[
          df_regions[col_name].astype(str).str.contains(search_query, na=False)
      ]
    else:
      filtered_df = df_regions

    st.markdown(
        f"<p style='color: #8b949e;'>عدد المناطق المتاحة: <b>{len(filtered_df)}</b></p>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # عرض المناطق في شكل كروت أو جدول منظم
    for index, row in filtered_df.iterrows():
      # عرض كل صف داخل كارت بروفيشنال
      card_content = "<div class='region-card'>"
      for col in df_regions.columns:
        val = row[col]
        if pd.notna(val):
          card_content += f"<p><b>{col}:</b> {val}</p>"
      card_content += "</div>"
      st.markdown(card_content, unsafe_allow_html=True)

  else:
    st.warning(
        "⚠️ جاري تحميل البيانات أو أن الجدول فارغ. تأكد من محتوى تبويب الشيت"
        " المرتبط."
    )

else:
  st.markdown("---")
  st.markdown("<h3>➕ إضافة وتعديل المناطق</h3>", unsafe_allow_html=True)
  st.info(
      "💡 لإضافة مناطق جديدة تظهر فوراً على التطبيق، قم بإضافتها مباشرة في ملف"
      " **Google Sheets** الخاص بك، وستظهر هنا لحظياً!"
  )
