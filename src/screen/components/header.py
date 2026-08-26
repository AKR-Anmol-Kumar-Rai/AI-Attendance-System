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

    logo_url= "https://i.pinimg.com/1200x/c8/46/ab/c846abb80b8c1d4459808c90af3a5c73.jpg"
    st.markdown(f"""
         <div style="display:flex; align-items:center; justify-content:center;gap:40px;"
            <img src='{logo_url}' style='height:85px;border-radius:10px;' />
            <h2 style-'text-align:left; color:#5865F2'>SNAP<br/>CLASS</h2>

         </div> 

    """,unsafe_allow_html=True)    