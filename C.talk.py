import streamlit as st
import pandas as pd
import html
import base64
from pathlib import Path

# تنظیمات صفحه
st.set_page_config(
    page_title="C.Talk",
    page_icon="🎟️",
    layout="centered"
)

# نام فایل اکسل
EXCEL_FILE = "attendees_list_2026-10-11_13_01_24_e719cd20ff0fff1cb7bcc011a30c8670.xlsx"

# خواندن تصویر پس‌زمینه
try:
    image_bytes = Path("c.jpg").read_bytes()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    background_image = f"url('data:image/jpeg;base64,{image_base64}')"
except FileNotFoundError:
    background_image = "none"

# طراحی ظاهری
st.markdown(
    f"""
    <style>
    .stApp {{
        background: linear-gradient(135deg, #4b0082, #8a2be2);
        min-height: 100vh;
    }}

    .stApp::before {{
        content: "";
        position: fixed;
        inset: 0;
        background-image: {background_image};
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        opacity: 0.3;
        pointer-events: none;
        z-index: 0;
    }}

    .stApp > header {{
        background: transparent;
    }}

    .stApp .main {{
        position: relative;
        z-index: 1;
    }}

    .block-container {{
        position: relative;
        z-index: 1;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }}

    h1 {{
        color: white;
        text-align: center;
        font-size: 3rem !important;
        font-weight: 800 !important;
    }}

    .subtitle {{
        color: white;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }}

    div[data-testid="stTextInput"] label {{
        color: white !important;
        font-size: 1.1rem;
        font-weight: bold;
    }}

    div[data-testid="stTextInput"] input {{
        border-radius: 12px;
        padding: 12px;
    }}

    .success-box {{
        background: rgba(255, 255, 255, 0.95);
        color: #222;
        padding: 25px;
        border-radius: 18px;
        text-align: center;
        margin-top: 25px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
    }}

    .success-box h2 {{
        color: #228B22;
        margin-bottom: 10px;
    }}

    .error-box {{
        background: rgba(255, 255, 255, 0.95);
        color: #b00020;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-top: 20px;
        font-weight: bold;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# عنوان برنامه
st.markdown("<h1>C.Talk</h1>", unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">به رویداد ما خوش آمدید</div>',
    unsafe_allow_html=True
)

# دریافت شماره بلیت
ticket_number = st.text_input(
    "شماره بلیت خود را وارد کنید",
    placeholder="شماره بلیت..."
)

# بررسی شماره بلیت
if ticket_number:
    try:
        df = pd.read_excel(EXCEL_FILE, engine="openpyxl")

        # تمیز کردن نام ستون‌ها
        df.columns = df.columns.astype(str).str.strip()

        required_columns = ["شماره بلیت", "نام", "نام خانوادگی"]

        if not all(col in df.columns for col in required_columns):
            st.error(
                "ستون‌های موردنیاز در فایل اکسل پیدا نشدند. "
                "لطفاً نام ستون‌ها را بررسی کنید."
            )
        else:
            # تبدیل شماره بلیت‌ها به رشته و حذف فاصله‌ها
            df["شماره بلیت"] = (
                df["شماره بلیت"]
                .fillna("")
                .astype(str)
                .str.strip()
                .str.replace(r"\.0$", "", regex=True)
            )

            entered_ticket = ticket_number.strip()

            # جست‌وجوی بلیت
            matched = df[df["شماره بلیت"] == entered_ticket]

            if not matched.empty:
                first_name = str(matched.iloc[0]["نام"]).strip()
                last_name = str(matched.iloc[0]["نام خانوادگی"]).strip()

                full_name = html.escape(
                    f"{first_name} {last_name}".strip()
                )

                st.markdown(
                    f"""
                    <div class="success-box">
                        <h2>✅ بلیت شما تأیید شد</h2>
                        <p style="font-size: 1.2rem;">
                            خوش آمدید، <strong>{full_name}</strong>
                        </p>
                        <p>از حضور شما در رویداد C.Talk خوشحالیم.</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    """
                    <div class="error-box">
                        ❌ شماره بلیت معتبر نیست.
                        لطفاً شماره بلیت خود را بررسی کنید.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    except FileNotFoundError:
        st.error(
            "فایل اکسل یا تصویر پس‌زمینه پیدا نشد. "
            "لطفاً فایل‌ها را در مسیر صحیح قرار دهید."
        )
    except Exception as e:
        st.error(f"خطا در خواندن اطلاعات: {e}")
