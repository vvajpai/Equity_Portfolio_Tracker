import re
import time
import hmac
import pandas as pd
import streamlit as st

from database_supa import add_stock, get_portfolio, remove_stock


st.set_page_config(page_title="Equity Portfolio Portal", page_icon="📈", layout="wide")

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        header[data-testid="stHeader"] {
            height: 0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

TICKER_PATTERN = re.compile(r"^[A-Z0-9.-]{1,20}$")
SESSION_TIMEOUT_SECONDS = 8 * 60 * 60


def get_auth_config() -> tuple[str, str]:
    auth_cfg = st.secrets.get("auth", {})

    username = str(auth_cfg.get("username", "")).strip()
    password = str(auth_cfg.get("password", ""))
    return username, password


def verify_password(password_input: str) -> bool:
    _, password = get_auth_config()
    return bool(password) and hmac.compare_digest(password_input, password)


def init_auth_state() -> None:
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "auth_username" not in st.session_state:
        st.session_state.auth_username = ""
    if "last_auth_ts" not in st.session_state:
        st.session_state.last_auth_ts = 0


def is_session_valid() -> bool:
    if not st.session_state.authenticated:
        return False

    now = int(time.time())
    age = now - int(st.session_state.last_auth_ts)
    return age <= SESSION_TIMEOUT_SECONDS


def show_login() -> None:
    cfg_username, cfg_password = get_auth_config()

    st.title("Portfolio Login")
    st.caption("Sign in to access your portfolio management portal.")

    if not cfg_username or not cfg_password:
        st.error(
            "Authentication is not configured. Set [auth].username and [auth].password "
            "in Streamlit Cloud Secrets."
        )
        st.stop()

    with st.form("login_form", clear_on_submit=True):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_clicked = st.form_submit_button("Login", type="primary", width="stretch")

    if login_clicked:
        user_ok = hmac.compare_digest(str(username).strip(), cfg_username)
        password_ok = verify_password(password)

        if user_ok and password_ok:
            st.session_state.authenticated = True
            st.session_state.auth_username = cfg_username
            st.session_state.last_auth_ts = int(time.time())
            st.rerun()
        else:
            st.error("Invalid username or password.")


def require_authentication() -> None:
    init_auth_state()

    if is_session_valid():
        st.session_state.last_auth_ts = int(time.time())
        return

    st.session_state.authenticated = False
    show_login()
    st.stop()


def normalize_ticker(ticker: str) -> str:
    return ticker.strip().upper()


def is_valid_ticker(ticker: str) -> bool:
    return bool(TICKER_PATTERN.match(ticker))


def load_portfolio() -> list[str]:
    portfolio = get_portfolio()
    return sorted(set(portfolio))


def show_portfolio_table(portfolio: list[str]) -> None:
    if not portfolio:
        st.info("No active stocks in your portfolio.")
        return

    df = pd.DataFrame({"Ticker": portfolio})
    st.dataframe(df, width="stretch", hide_index=True)


require_authentication()

with st.sidebar:
    st.success(f"Logged in as: {st.session_state.auth_username}")
    if st.button("Logout", width="stretch"):
        st.session_state.authenticated = False
        st.session_state.auth_username = ""
        st.session_state.last_auth_ts = 0
        st.rerun()

st.title("Equity Portfolio Tracker Portal")
st.caption("Add or remove stocks from your Supabase portfolio.")

if "portfolio" not in st.session_state:
    st.session_state.portfolio = load_portfolio()

col_left, col_right = st.columns([2, 1], gap="large")

with col_left:
    st.subheader("Current Portfolio")
    with st.expander(
        f"Portfolio Card ({len(st.session_state.portfolio)} stocks)",
        expanded=True,
    ):
        show_portfolio_table(st.session_state.portfolio)

    if st.button("Refresh Portfolio", width="stretch"):
        st.session_state.portfolio = load_portfolio()
        st.success("Portfolio refreshed.")

with col_right:
    st.subheader("Manage Stocks")
    st.write("Enter ticker symbol such as `TCS.NS` or `AAPL`.")

    with st.form("add_stock_form", clear_on_submit=True):
        new_ticker = st.text_input("Ticker to add", key="add_ticker")
        add_clicked = st.form_submit_button("Add Stock", type="primary", width="stretch")

    if add_clicked:
        ticker = normalize_ticker(new_ticker)

        if not ticker:
            st.warning("Please enter a ticker.")
        elif not is_valid_ticker(ticker):
            st.warning("Ticker format is invalid. Use letters, numbers, dot or hyphen.")
        elif ticker in st.session_state.portfolio:
            st.info(f"{ticker} is already in the portfolio.")
        else:
            ok = add_stock(ticker)
            if ok:
                st.session_state.portfolio = load_portfolio()
                st.success(f"Added {ticker} to portfolio.")
            else:
                st.error("Failed to add stock. Check Supabase constraints or credentials.")

    st.divider()

    if not st.session_state.portfolio:
        st.info("No stocks available to remove.")
    else:
        with st.form("remove_stock_form"):
            ticker_to_remove = st.selectbox(
                "Select ticker to remove",
                options=st.session_state.portfolio,
                index=0,
                key="remove_ticker",
            )
            remove_clicked = st.form_submit_button("Remove Stock", width="stretch")

        if remove_clicked:
            ok = remove_stock(ticker_to_remove)
            if ok:
                st.session_state.portfolio = load_portfolio()
                st.success(f"Removed {ticker_to_remove} from portfolio.")
            else:
                st.error("Failed to remove stock. Please try again.")
