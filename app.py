import math
import streamlit as st

page_style = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://i.ibb.co/V0qp0ZjP/file-000000003cb0622fa742531d697013d9.png");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-position: center;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);  /* شفاف‌سازی هدر */
}
</style>
"""
st.markdown(page_style, unsafe_allow_html=True)


st.set_page_config(page_title="CalcFinity • Aifinity", page_icon="💹")

st.title("💹 ماشین‌حساب مدیریت سرمایه - Aifinity")
st.caption("محاسبه ریسک ۱/۲/۳٪، حجم پوزیشن و مارجین ورودی با گرد کردن به عدد صحیح یا نیم‌واحد")

# ورودی‌ها
col1, col2 = st.columns(2)
with col1:
    balance = st.number_input("💰 دارایی (USDT)", min_value=0.0, value=0.0, step=0.01, format="%.2f")
with col2:
    sl_percent = st.number_input("⛔ درصد استاپ‌لاس (%)", min_value=0.0, value=2.0, step=0.1, format="%.2f")

risk_choice = st.radio("⚠️ انتخاب ریسک", [1, 2, 3], index=0, horizontal=True)
round_step = st.selectbox("🔁 گام گرد کردن مارجین", [1.0, 0.5], index=0, format_func=lambda x: "۱ (عدد صحیح)" if x==1.0 else "۰.۵ (نیم‌واحد)")

st.divider()

# محاسبات
def floor_to_step(x: float, step: float) -> float:
    return math.floor(x / step) * step

# ریسک‌ها: دو رقم اعشار مثل نمونه بات
r1 = round(balance * 0.01, 2)
r2 = round(balance * 0.02, 2)
r3 = round(balance * 0.03, 2)
risk_map = {1: r1, 2: r2, 3: r3}
risk_amount = risk_map[risk_choice]

# نمایش ریسک‌ها
st.subheader("ریسک‌ها (بر اساس دارایی)")
st.write(f"• 1% → **{r1:.2f}**   |   2% → **{r2:.2f}**   |   3% → **{r3:.2f}**")

if sl_percent <= 0:
    st.warning("لطفاً درصد استاپ‌لاس را بزرگ‌تر از صفر وارد کن.")
else:
    pos_size = risk_amount / (sl_percent / 100.0) if sl_percent > 0 else 0.0
    margin_floor_1 = floor_to_step(pos_size, 1.0)
    margin_floor_05 = floor_to_step(pos_size, 0.5)
    margin_selected = floor_to_step(pos_size, round_step)

    st.subheader("نتایج محاسبه")
    st.markdown(f"""
- ریسک انتخابی: **{risk_choice}% = {risk_amount:.2f}**
- حجم پوزیشن (Risk / SL%): **{pos_size:.6f}**
- مارجین ورودی (گرد به پایین با گام انتخابی): **{margin_selected:.2f}**
""")

    with st.expander("جزئیات گرد کردن"):
        st.write(f"- گرد به عدد صحیح (گام 1): **{margin_floor_1:.2f}**")
        st.write(f"- گرد به نیم‌واحد (گام 0.5): **{margin_floor_05:.2f}**")

st.info("نکته: مثل نمونه بات، ریسک‌ها به دو رقم اعشار نمایش داده می‌شوند و مارجین بر اساس گام انتخابی به **پایین** گرد می‌شود.")
