from datetime import datetime

import streamlit as st

NAME = "Muhammad Haseeb"      # change these four lines to customise
ACCOUNT = "1234567890"
PIN = "1234"
START_BALANCE = 5000
CUR = "Rs."

st.set_page_config(page_title="ATM Machine", page_icon="🏧", layout="centered")
st.markdown(
    """<style>
    .stApp{background:radial-gradient(circle at 50% 0%,#14224a,#050816 70%)}
    header,footer,#MainMenu{visibility:hidden}
    h1,h2,h3,p,label,span,div{color:#e9eefc}
    .screen{background:#06122b;border:2px solid #2d4a9a;border-radius:16px;padding:22px;
      text-align:center;box-shadow:0 0 28px #2d4a9a55 inset;margin:8px 0 16px}
    .big{font-size:2.3rem;font-weight:800;color:#6dffb2;text-shadow:0 0 14px #6dffb299}
    .title{font-size:2rem;font-weight:800;text-align:center;letter-spacing:1px}
    .stButton>button{width:100%;border-radius:12px;border:1px solid #f5b83d;background:#0b1636;
      color:#f5b83d;font-weight:700;padding:.6rem}
    .stButton>button:hover{background:#f5b83d;color:#050816}
    </style>""",
    unsafe_allow_html=True,
)

ss = st.session_state
for k, v in {"auth": False, "tries": 0, "balance": START_BALANCE, "screen": "menu", "history": [], "bye": False}.items():
    ss.setdefault(k, v)


def log(kind, amount):
    ss.history.insert(0, {"Time": datetime.now().strftime("%d %b %H:%M"), "Type": kind,
                          "Amount": f"{CUR}{amount:,.0f}", "Balance": f"{CUR}{ss.balance:,.0f}"})


def go(screen):
    ss.screen = screen


st.markdown('<div class="title">🏧 ATM Machine</div>', unsafe_allow_html=True)

if ss.bye:
    st.markdown('<div class="screen">Thank you for using the ATM.<br>Have a nice day! 👋</div>', unsafe_allow_html=True)
    if st.button("Start again"):
        ss.update(auth=False, tries=0, screen="menu", bye=False)
        st.rerun()

elif not ss.auth:
    if ss.tries >= 3:
        st.markdown('<div class="screen">🔒 Card blocked after 3 wrong PIN attempts.</div>', unsafe_allow_html=True)
        if st.button("Reset card"):
            ss.tries = 0
            st.rerun()
    else:
        st.markdown('<div class="screen">Please enter your PIN</div>', unsafe_allow_html=True)
        with st.form("pin"):
            pin = st.text_input("Enter PIN", type="password", max_chars=4)
            if st.form_submit_button("Enter"):
                if pin == PIN:
                    ss.auth = True
                else:
                    ss.tries += 1
                    st.error(f"Wrong PIN. {3 - ss.tries} attempt(s) left.")
                if ss.auth:
                    st.rerun()
        st.caption("Demo PIN: 1234")

elif ss.screen == "menu":
    st.markdown('<div class="screen">Welcome, <b>%s</b><br>Choose an option</div>' % NAME, unsafe_allow_html=True)
    for label, target in [("1. Check Balance", "balance"), ("2. Deposit", "deposit"),
                          ("3. Withdraw", "withdraw"), ("4. Account Details", "details")]:
        st.button(label, on_click=go, args=(target,))
    if st.button("5. Exit"):
        ss.bye = True
        st.rerun()

else:
    s = ss.screen
    if s == "balance":
        st.markdown(f'<div class="screen">Your Balance<div class="big">{CUR}{ss.balance:,.0f}</div></div>', unsafe_allow_html=True)
    elif s in ("deposit", "withdraw"):
        st.markdown(f'<div class="screen">{s.title()}<div class="big">{CUR}{ss.balance:,.0f}</div>available</div>', unsafe_allow_html=True)
        with st.form(s):
            amount = st.number_input(f"Enter amount ({CUR})", min_value=0.0, step=100.0)
            if st.form_submit_button(s.title()):
                if amount <= 0:
                    st.warning("Enter an amount greater than 0.")
                elif s == "deposit":
                    ss.balance += amount
                    log("Deposit", amount)
                    st.success(f"Deposited: {CUR}{amount:,.0f} | New Balance: {CUR}{ss.balance:,.0f}")
                elif amount <= ss.balance:
                    ss.balance -= amount
                    log("Withdraw", amount)
                    st.success(f"Withdrawn: {CUR}{amount:,.0f} | Remaining Balance: {CUR}{ss.balance:,.0f}")
                else:
                    st.error("Insufficient balance.")
    elif s == "details":
        st.markdown(f'<div class="screen">Name: <b>{NAME}</b><br>Account Number: <b>{ACCOUNT}</b></div>', unsafe_allow_html=True)
        st.subheader("Mini statement")
        if ss.history:
            st.dataframe(ss.history[:10], use_container_width=True, hide_index=True)
        else:
            st.caption("No transactions yet.")
    st.button("⬅ Back to menu", on_click=go, args=("menu",))
