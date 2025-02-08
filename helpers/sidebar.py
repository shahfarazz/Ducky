import base64
import streamlit as st


def get_image_b64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')


def show() -> None:
    logo_b64 = get_image_b64("static/logo.png")
    with st.sidebar:
        st.markdown(f"""
                        <a href="/" style="color:black;text-decoration: none;">
                                        <div style="display:table;margin-top:-16rem;margin-left:0%;">
                                                        <img src="data:image/png;base64,{logo_b64}" width="60"><span style ="color: white">&nbsp;&nbsp;Ducky</span>
                                                        <span style="font-size: 0.8em; color: white">&nbsp;&nbsp;v0.1.0</span>
                                                        <br>
                        </a>
                        <br>
                                        """, unsafe_allow_html=True)

        reload_button = st.button("↪︎  Reload Page")
        if reload_button:
            st.session_state.clear()
            st.experimental_rerun()
