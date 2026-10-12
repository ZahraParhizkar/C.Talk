
import streamlit as st
import pandas as pd
import html


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
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 800px;
    }

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

    .input-label {
        font-size: 22px;
        font-weight: 700;
        color: #4c1d95;
        margin-bottom: 10px;
        text-align: center;
    }

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

    .welcome-box {
        margin-top: 20px;
        padding: 15px 0;
        text-align: center;
        direction: rtl;
        color: #581c87;
        font-size: 27px;
        font-weight: 800;
        white-space: normal;
    }

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
# عنوان برنامه
# =========================================================

st.markdown(
    '<div class="ctalk-title">C.Talk</div>',
    unsafe_allow_html=True
)


# =========================================================
# مسیر فایل Excel
# فایل Excel باید کنار فایل پایتون در GitHub باشد
# =========================================================

FILE_NAME = (
    "attendees_list_2026-10-11_13_01_24_"
    "e719cd20ff0fff1cb7bcc011a30c8670.xlsx"
)


# =========================================================
# خواندن فایل Excel
# =========================================================

try:
    df = pd.read_excel(
        FILE_NAME,
        engine="openpyxl",
        dtype={"شماره بلیت": str}
    )

except FileNotFoundError:
    st.error(f"فایل Excel پیدا نشد: {FILE_NAME}")
    st.stop()

except ImportError:
    st.error(
        "کتابخانه openpyxl نصب نیست. "
        "فایل requirements.txt را بررسی کنید."
    )
    st.stop()

except Exception as e:
    st.error(f"خطا در خواندن فایل Excel: {e}")
    st.stop()


# =========================================================
# تمیز کردن نام ستون‌ها
# =========================================================

df.columns = df.columns.astype(str).str.strip()


# =========================================================
# بررسی ستون‌های موردنیاز
# =========================================================

required_columns = [
    "شماره بلیت",
    "نام",
    "نام خانوادگی"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(
        "ستون‌های زیر در فایل Excel پیدا نشدند: "
        + "، ".join(missing_columns)
    )

    st.write(
        "ستون‌های موجود در فایل Excel:",
        df.columns.tolist()
    )

    st.stop()


# =========================================================
# آماده‌سازی شماره بلیت برای جستجو
# =========================================================

df["_code_for_search"] = (
    df["شماره بلیت"]
    .astype("string")
    .str.strip()
    .str.replace(r"\.0$", "", regex=True)
)


# =========================================================
# عنوان و ورودی شماره بلیت
# =========================================================

st.markdown(
    '<div class="input-label">کد خود را وارد کنید</div>',
    unsafe_allow_html=True
)

user_code = st.text_input(
    "شماره بلیت",
    placeholder="مثلاً 123456",
    label_visibility="collapsed"
)


# =========================================================
# بررسی شماره بلیت
# =========================================================

if user_code:

    user_code = user_code.strip()

    matched_rows = df[
        df["_code_for_search"] == user_code
    ]

    # -----------------------------------------------------
    # شماره بلیت معتبر است
    # -----------------------------------------------------

    if not matched_rows.empty:

        person = matched_rows.iloc[0]

        first_name = (
            ""
            if pd.isna(person["نام"])
            else str(person["نام"]).strip()
        )

        last_name = (
            ""
            if pd.isna(person["نام خانوادگی"])
            else str(person["نام خانوادگی"]).strip()
        )

        person_name = f"{first_name} {last_name}".strip()

        # نمایش تأیید
        st.markdown(
            """
            <div class="success-box">
                ✓ &nbsp; تأیید شد
            </div>
            """,
            unsafe_allow_html=True
        )

        # نمایش نام کامل و پیام خوش‌آمدگویی
        safe_name = html.escape(person_name)

        st.markdown(
            f"""
            <div class="welcome-box">
                {safe_name} عزیز،
                به رویداد C.Talk خوش آمدید! 🎉
            </div>
            """,
            unsafe_allow_html=True
        )

    # -----------------------------------------------------
    # شماره بلیت معتبر نیست
    # -----------------------------------------------------

    else:

        st.markdown(
            """
            <div class="error-box">
                ✕ &nbsp; این کد در سیستم وجود ندارد
            </div>
            """,
            unsafe_allow_html=True
        )
