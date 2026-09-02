import streamlit as st
from src.screen.database.db import create_subject
import segno
import io

@st.dialog("SHARE CLASS LINK")
def share_subject_dialog(subject_name, subject_code):
    app_domain = "ai-attendance01.streamlit.app"
    join_url = f"{app_domain}/?join-code={subject_code}"

    st.header("SCAN TO JOIN")
    st.space()

    qr= segno.make(join_url)

    out = io.BytesIO()   # This creates a memory buffer (like a fake file) and qr is saved into this memeory

    qr.save(out, kind="png", scale=10, border=1)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Copy Link")
        st.code(join_url, language='text')
        st.code(subject_code, language='text')
        st.info("Copy this link to share on Whatsapp or Email")

    with col2:
        st.markdown("### Scan to Join")
        st.image(out.getvalue(), caption="QRCODE for Class Joining")   #  st.image(out.getvalue()) => Convert memory → image



   