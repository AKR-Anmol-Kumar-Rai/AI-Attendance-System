import streamlit as st

def header_home():

    logo_url= "https://file.aiquickdraw.com/imgcompressed/img/compressed_a5696edabf377d67655b27a15eafa353.webp"
    st.markdown(f"""
         <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-border:30px; margin-top:0px; padding-bottom:0px;text-align:center;">
                
            <img src='{logo_url}' style='height:70px;border-radius:10px;' />
             <h1 style='text-align:center; color:#E0E3FF'>AI<br/><span style="padding-left:32px;">ATTENDANCE</span></h1>

         </div> 

    """,unsafe_allow_html=True)


def header_dashboard():

    logo_url="https://file.aiquickdraw.com/imgcompressed/img/compressed_a5696edabf377d67655b27a15eafa353.webp"

    # Take this whole box and move it 30 pixels upward
    st.markdown("""
        <style>
            div[data-testid="stMarkdown"] {
            margin-top: -40px !important;
            }
        </style>
        """, unsafe_allow_html=True)

    # div makes the container/box
    st.markdown(f"""
         <div style="display:flex; align-items:center; justify-content:center;gap:10px;">
            <img src='{logo_url}' style='height:85px;border-radius:10px;' />
            <h2 style='text-align:left; color:#5865F2'><span style="padding-left:90px;">AI</span> <br/> ATTENDANCE</h2>

         </div> 

    """,unsafe_allow_html=True)    