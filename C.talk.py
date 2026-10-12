import streamlit as st
import pandas as pd


# =========================================================
# تنظیمات صفحه
# =========================================================

st.set_page_config(
    page_title="C.Talk",
    page_icon="✓",
    layout="centered"
)


# =========================================================
# CSS و طراحی صفحه
# =========================================================

st.markdown(
    """
    <style>

    /* محدود کردن عرض صفحه */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 800px;
    }


    /* =====================================================
       پس زمینه کل برنامه
       ===================================================== */

    .stApp {
        background: linear-gradient(
            135deg,
            #f3e8ff 0%,
            #e9d5ff 35%,
            #c084fc 70%,
            #7e22ce 100%
        );

        min-height: 100vh;
    }


    /* =====================================================
       عنوان C.Talk
       ===================================================== */

    .ctalk-title {

        text-align: center;

        font-size: 90px;

        font-weight: 900;

        margin-top: 30px;

        margin-bottom: 50px;

        background: linear-gradient(
            90deg,
            #4c1d95,
            #7e22ce,
            #a855f7,
            #c084fc,
            #6d28d9
        );

        -webkit-background-clip: text;

        -webkit-text-fill-color: transparent;

        background-clip: text;
    }

    /* =====================================================
       عنوان بالای کادر ورود کد
       ===================================================== */

    .input-label {

        font-size: 22px;

        font-weight: 700;

        color: #4c1d95;

        margin-bottom: 10px;

        text-align: center;
    }


    /* =====================================================
       نتیجه تأیید
       ===================================================== */

    .success-box {

        margin-top: 30px;

        padding: 25px;

        border-radius: 18px;

        background: linear-gradient(
            90deg,
            #dcfce7,
            #bbf7d0
        );

        border: 2px solid #22c55e;

        text-align: center;

        color: #166534;

        font-size: 30px;

        font-weight: 800;
    }


    /* =====================================================
       پیام خوش آمدگویی
       بدون کادر و بدون پس زمینه
       ===================================================== */

    .welcome-box {

        margin-top: 20px;

        padding: 15px 0;

        background: transparent;

        border: none;

        border-radius: 0;

        text-align: center;

        direction: rtl;

        color: #581c87;

        font-size: 27px;

        font-weight: 800;

        white-space: nowrap;
    }


    /* =====================================================
       نتیجه عدم تأیید
       ===================================================== */

    .error-box {

        margin-top: 30px;

        padding: 25px;

        border-radius: 18px;

        background: linear-gradient(
            90deg,
            #fee2e2,
            #fecaca
        );

        border: 2px solid #ef4444;

        text-align: center;

        color: #991b1b;

        font-size: 25px;

        font-weight: 700;
    }


    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# عنوان
# =========================================================

st.markdown(
    '<div class="ctalk-title">C.Talk</div>',
    unsafe_allow_html=True
)


# =========================================================
# خواندن فایل Excel
# =========================================================

FILE_NAME = r"attendees_list_2026-10-11_13_01_24_e719cd20ff0fff1cb7bcc011a30c8670.xlsx"


try:

    df = pd.read_excel(FILE_NAME)


except FileNotFoundError:

    st.error(
        f"فایل Excel پیدا نشد:\n{FILE_NAME}"
    )

    st.stop()


except Exception as e:

    st.error(
        f"خطا در خواندن فایل Excel: {e}"
    )

    st.stop()


# =========================================================
# تمیز کردن نام ستون‌ها
# =========================================================

df.columns = (
    df.columns
    .astype(str)
    .str.strip()
)


# =========================================================
# پیدا کردن ستون «کد»
# =========================================================

code_column = None


for column in df.columns:

    if column.strip() == "شماره بلیت":

        code_column = column

        break


if code_column is None:

    st.error(
        "ستون «کد» در فایل Excel پیدا نشد."
    )

    st.stop()


# =========================================================
# پیدا کردن ستون «نام»
# =========================================================

name_column = None


# ابتدا ستون دقیقاً «نام»
for column in df.columns:

    if column.strip() == "نام":

        name_column = column

        break


# اگر «نام» وجود نداشت،
# چند نام رایج دیگر را بررسی می‌کنیم

if name_column is None:

    possible_name_columns = [

        "نام و نام خانوادگی",

        "نام‌",

        "نام خانوادگی",

        "اسم",

        "Name",

        "name"
    ]


    for possible_column in possible_name_columns:

        if possible_column in df.columns:

            name_column = possible_column

            break


# اگر هیچ ستون نامی پیدا نشد

if name_column is None:

    st.error(
        "ستون مربوط به نام شخص در فایل Excel پیدا نشد."
    )

    st.write(
        "ستون‌های موجود در فایل Excel:",
        df.columns.tolist()
    )

    st.stop()


# =========================================================
# آماده سازی ستون کد برای جستجو
# =========================================================

df["_code_for_search"] = (

    df[code_column]

    .astype(str)

    .str.strip()
)


# =========================================================
# کارت اصلی
# =========================================================

st.markdown(
    '<div class="main-card">',
    unsafe_allow_html=True
)


# =========================================================
# عنوان ورودی
# =========================================================

st.markdown(
    '<div class="input-label">کد خود را وارد کنید</div>',
    unsafe_allow_html=True
)


# =========================================================
# ورودی کد
# =========================================================

user_code = st.text_input(

    "",

    placeholder="مثلاً 123456",

    label_visibility="collapsed"
)


# =========================================================
# بررسی کد
# =========================================================

if user_code:

    user_code = user_code.strip()


    # =====================================================
    # پیدا کردن ردیف مربوط به کد
    # =====================================================

    matched_rows = df[
        df["_code_for_search"] == user_code
    ]


    # =====================================================
    # اگر کد پیدا شد
    # =====================================================

    if not matched_rows.empty:


        # -----------------------------------------------
        # گرفتن نام از همان ردیف
        # -----------------------------------------------

        person_name = str(
            matched_rows.iloc[0][name_column]
        ).strip()


        # -----------------------------------------------
        # نمایش تأیید
        # -----------------------------------------------

        st.markdown(
            """
            <div class="success-box">
                ✓ &nbsp; تأیید شد
            </div>
            """,

            unsafe_allow_html=True
        )


        # -----------------------------------------------
        # نمایش پیام خوش آمدگویی
        # -----------------------------------------------

        st.markdown(
            f"""
            <div class="welcome-box">
                {person_name} عزیز، به رویداد C.Talk خوش آمدید! 🎉
            </div>
            """,

            unsafe_allow_html=True
        )


    # =====================================================
    # اگر کد پیدا نشد
    # =====================================================

    else:

        st.markdown(
            """
            <div class="error-box">
                ✕ &nbsp; این کد در سیستم وجود ندارد
            </div>
            """,

            unsafe_allow_html=True
        )


# =========================================================
# پایان کارت
# =========================================================

st.markdown(
    '</div>',
    unsafe_allow_html=True
)
